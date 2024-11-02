import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Тест для проверки главной страницы
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 404  # Так как у нас нет главной страницы, ожидаем 404

# Тест для маршрута, возвращающего данные
def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b'This is some data!' in response.data

# Тест для получения существующего пользователя
def test_get_user(client):
    # Создайте тестового пользователя, чтобы убедиться, что он есть в базе данных
    response = client.post('/users', json={'username': 'john_doe', 'email': 'john@example.com'})
    assert response.status_code == 200

    # Проверьте, что маршрут /users/1 возвращает данные этого пользователя
    response = client.get('/users/1')
    assert response.status_code == 200
    assert b'john_doe' in response.data

def test_cache(client):
    response1 = client.get('/data')
    response2 = client.get('/data')
    assert response1.data == response2.data # Данные должны быть одинаковыми из-за кэша

# Тест для маршрута 404
def test_404(client):
    response = client.get('/non_existent_route')
    assert response.status_code == 404
