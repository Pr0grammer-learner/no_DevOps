from app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Тест для маршрута, возвращающего данные
def test_data_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This is some data!' in response.data

# # Тест кэширования
# def test_cache(client):
#     response1 = client.get('/data')
#     response2 = client.get('/data')
#     # Данные должны быть одинаковыми из-за кэширования
#     assert response1.data == response2.data

# Тест для маршрута 404
def test_404(client):
    response = client.get('/non_existent_route')
    assert response.status_code == 404
