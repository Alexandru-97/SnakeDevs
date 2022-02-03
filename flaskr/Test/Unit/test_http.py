import pytest
import json
from app import create_app

# python -m pytest -v Test/Unit/test_http.py


def login(client):
    payload = {'username': 'stefan', 'password': 'parola'}
    client.post('/auth/login', data=payload, follow_redirects=True)


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """
    # app.config['TESTING'] = True
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Hello User, not World!' in html
    assert landing.status_code == 200

def test_set_auth(client):
    payload = {'username': 'stefan', 'password': 'parola'}
    rv = client.post('/auth/login', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'user logged in succesfully'

def test_get_temperature(client):
    login(client)
    request = client.get("/temperature/")
    assert request.status_code == 200

def test_set_temperature(client):
    login(client)
    payload = {'value': 100}
    rv = client.post('/temperature/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Temperature successfully recorded/retrieved'

def test_get_rgb(client):
    login(client)
    request = client.get("/rgb/")
    assert request.status_code == 200

def test_set_rgb(client):
    login(client)
    payload = {'red': 100, 'green': 100, 'blue': 100}
    rv = client.post('/rgb/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "RGB successfully recorded/retrieved"

def test_get_holiday(client):
    login(client)
    request = client.get("/holiday/")
    assert request.status_code == 200

def test_set_holiday(client):
    login(client)
    payload = {'is_away': True, 'days': 10}
    rv = client.post('/holiday/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Holiday successfully recorded/retrieved'

def test_get_stock(client):
    login(client)
    request = client.get("/stock/")
    assert request.status_code == 200

def test_set_stock(client):
    login(client)
    payload = {'product_name': 'carne' , 'quantity': 10, 'product_expiration_date': "2022-03-27 13:37:24", 'shelf_number': 3}
    rv = client.post('/stock/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert res["status"] == 'Stock successfully recorded/retrieved'

def test_get_timer(client):
    login(client)
    request = client.get("/timer/")
    assert request.status_code == 200

def test_set_timer(client):
    login(client)
    payload = {'is_closed': True, 'time': 10}
    rv = client.post('/timer/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Timer successfully recorded/retrieved'

def test_get_expired(client):
    login(client)
    request = client.get("/stock/expired")
    assert request.status_code == 200
