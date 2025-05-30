import pytest
from fastapi.testclient import TestClient

from .main import app


@pytest.fixture
def test_data():
    return {'key': 'mykey', 'value': 'myvalue'}


@pytest.mark.integtest
def test_set_string(test_data):
    with TestClient(app) as client:
        response = client.post('/strset/', json=test_data)
        assert response.status_code == 200
        assert response.json()


@pytest.mark.integtest
def test_get_string_existing(test_data):
    with TestClient(app) as client:
        client.post('/strset/', json=test_data)
        response = client.post('/strget/', json=test_data)

        assert response.status_code == 200
        data = response.json()
        assert data == 'myvalue'


@pytest.mark.integtest
def test_get_string_missing():
    with TestClient(app) as client:
        response = client.post('/strget/', json={'key': 'not_existing_key'})
        assert response.json() == ''
