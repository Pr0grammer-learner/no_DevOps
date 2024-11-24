from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics
from Token_generator import TokenGenerator
import os
import socket


app = Flask(__name__)
metrics = PrometheusMetrics(app)
# Настройки базы данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Настройка кэша (Redis как backend для кэша)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = os.getenv('REDIS_HOST', 'localhost')
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = f"redis://{app.config['CACHE_REDIS_HOST']}:{app.config['CACHE_REDIS_PORT']}/0"

# Инициализация кэша
cache = Cache(app)
token_generator = TokenGenerator()

@app.route('/health')
def health_check():
    return jsonify(status="OK"), 200

@app.route('/container_id')
def get_container_id():
    return jsonify({'container_id': socket.gethostname()})

# Определение модели User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Пример маршрута с кэшированием
@app.route('/api/access')
@cache.cached(timeout=300)  # Данные будут кэшироваться на 5 минут
def get_data():
    # Получение уникального токена
    user_token = token_generator.generate_token()
    return jsonify({'your_token': user_token})

# CRUD операции
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
@cache.cached(timeout=120, key_prefix='all_users')  # Кэшируем список пользователей на 120 секунд
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list)

@app.route('/users/<int:id>', methods=['GET'])
@cache.cached(timeout=120, key_prefix='user_data')  # Кэшируем запрос к пользователю по ID на 120 секунд
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@app.route('/del/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    cache.delete(f'user_data/{id}')
    cache.delete('all_users')

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {id} deleted successfully'})

@app.route('/')
def main_page():
    return render_template('docs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
