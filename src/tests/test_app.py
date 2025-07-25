import sys
import os
import json
import pytest

# Add parent directory to path to import the app correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import directly from app module, not src.app
from app import app, init_app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost.localdomain'  # Needed for URL generation
    with app.app_context():
        init_app()  # Initialize the app with test configuration
        with app.test_client() as client:
            yield client

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'

def test_get_messages(client):
    response = client.get('/api/messages')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_add_message(client):
    # Test with valid data
    response = client.post(
        '/api/messages',
        data=json.dumps({'content': 'Test message'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['content'] == 'Test message'

    # Test with invalid data
    response = client.post(
        '/api/messages',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400 