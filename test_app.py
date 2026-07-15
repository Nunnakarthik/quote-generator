import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the homepage loads and shows the quote card"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Quote of the Day" in response.data

def test_random_quote(client):
    """Test that /quote returns a valid quote with required fields"""
    response = client.get('/quote')
    assert response.status_code == 200
    data = response.get_json()
    assert 'quote' in data
    assert 'author' in data

def test_quote_of_the_day(client):
    """Test that /quote/today returns a valid quote"""
    response = client.get('/quote/today')
    assert response.status_code == 200
    data = response.get_json()
    assert 'quote' in data
    assert 'author' in data