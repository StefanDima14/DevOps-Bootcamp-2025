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
    with patch('app.boto3.resource') as mocked_resource:
        mock_table = mocked_resource.return_value.Table.return_value
        mock_table.scan.return_value = {'Items': []}
        response = client.get('/')
        assert response.status_code == 200
        assert b"LinkStack" in response.data

def test_add_link_redirect(client):
    """Test that adding a link redirects to home."""
    with patch('app.boto3.resource') as mocked_resource:
        mock_table = mocked_resource.return_value.Table.return_value
        response = client.post('/add', data={
            'title': 'Google',
            'url': 'https://google.com'
        })
        assert response.status_code == 302 # Redirect
        mock_table.put_item.assert_called_once()