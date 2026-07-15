import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the homepage loads and returns expected message"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Welcome to the Quote Generator API!"

def test_random_quote(client):
    """Test that /quote returns a valid quote with required fields"""
    response = client.get('/quote')
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'quote' in data
    assert 'author' in data

def test_quote_by_valid_id(client):
    """Test fetching a specific quote that exists"""
    response = client.get('/quote/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['author'] == "Steve Jobs"

def test_quote_by_invalid_id(client):
    """Test fetching a quote that doesn't exist"""
    response = client.get('/quote/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Quote not found"