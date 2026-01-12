import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the homepage loads."""
    with patch('app.table.scan') as mocked_scan:
        mocked_scan.return_value = {'Items': []}
        response = client.get('/')
        assert response.status_code == 200
        assert b"LinkStack" in response.data

def test_add_link_redirect(client):
    """Test that adding a link redirects to home."""
    with patch('app.table.put_item') as mocked_put:
        response = client.post('/add', data={
            'title': 'Google',
            'url': 'https://google.com'
        })
        assert response.status_code == 302 # Redirect
        mocked_put.assert_called_once()