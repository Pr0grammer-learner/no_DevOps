import pytest
from app import app, db

# Настройка приложения для тестирования
@pytest.fixture
def client():
    # Изменяем конфигурацию для использования SQLite в памяти
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Создаем все таблицы для тестовой БД
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Удаляем все таблицы после тестов

# Тест для проверки главной страницы
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200  # Ожидаем код 200 для главной страницы
    assert b'Добро пожаловать в документацию API для mirea-api.ru' in response.data  # Проверяем содержимое docs.html

# Тест для маршрута, возвращающего данные
def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b'This is some data!' in response.data

# Тест для создания и получения пользователя
def test_get_user(client):
    # Создайте тестового пользователя, чтобы убедиться, что он есть в базе данных
    response = client.post('/users', json={'username': 'john_doe', 'email': 'john@example.com'})
    assert response.status_code == 200

    # Проверьте, что маршрут /users/1 возвращает данные этого пользователя
    response = client.get('/users/1')
    assert response.status_code == 200
    assert b'john_doe' in response.data

# Тест для кэша
def test_cache(client):
    response1 = client.get('/data')
    response2 = client.get('/data')
    assert response1.data == response2.data  # Данные должны быть одинаковыми из-за кэша

# Тест для маршрута 404
def test_404(client):
    response = client.get('/non_existent_route')
    assert response.status_code == 404
