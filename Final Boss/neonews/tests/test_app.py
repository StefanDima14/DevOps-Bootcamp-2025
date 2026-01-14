import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get_page(client):
    """Test that the homepage loads on a GET request."""
    response = client.get('/')
    assert response.status_code == 200
    # Assuming your index.html contains the title "NeoNews"
    assert b"NeoNews" in response.data

@patch('app.threading.Thread')
@patch('app.api.get_news')
@patch('app.api.get_country_details')
def test_index_post_page(mock_get_country, mock_get_news, mock_thread, client):
    """Test a successful POST request to the index page."""
    # Arrange: Configure the return values of our mocked functions
    mock_get_country.return_value = {'cca2': 'US', 'name': 'United States'}
    mock_get_news.return_value = [{'title': 'Test Article', 'link': 'http://example.com'}]

    # Act: Simulate a user submitting the form
    response = client.post('/', data={'country': 'USA', 'topic': 'business', 'language': 'en'})

    # Assert: Check the outcomes
    assert response.status_code == 200
    assert b"Success! Found 1 articles" in response.data
    assert b"Test Article" in response.data
    mock_get_country.assert_called_once_with('USA')
    mock_get_news.assert_called_once_with('US', 'business', 'en')
    mock_thread.assert_called_once()