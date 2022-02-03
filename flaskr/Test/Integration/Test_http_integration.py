import pytest
import json
from app import create_app

# python -m pytest -v Test/Integration/Test_http_integration.py
# python -m pytest -v

def login(client):
    payload = {'username': 'stefan', 'password': 'parola'}
    client.post('/auth/login', data=payload, follow_redirects=True)


def in_stock(data, product_name, quantity):
    ok = False
    for product in data['data']:
        if product['product_name'] == product_name and product['quantity'] == quantity:
            ok = True
    return ok

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


def test_temperature(client):
    login(client)

    payload = {'value': 1}
    rv = client.post('/temperature/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Temperature successfully recorded/retrieved'

    request = client.get("/temperature/", follow_redirects=True)
    data = json.loads(request.data)
    assert request.status_code == 200
    assert data['data']['value'] == 1


def test_rgb(client):
    login(client)

    payload = {'red': 100, 'green': 100, 'blue': 100}
    rv = client.post('/rgb/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "RGB successfully recorded/retrieved"

    request = client.get("/rgb/")
    assert request.status_code == 200
    data = json.loads(request.data)
    assert data['data']['red'] == 100 and data['data']['red'] == 100 and data['data']['red'] == 100


def test_holiday(client):
    login(client)

    payload = {'is_away': True, 'days': 10}
    rv = client.post('/holiday/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Holiday successfully recorded/retrieved'

    request = client.get("/holiday/")
    assert request.status_code == 200
    data = json.loads(request.data)
    assert data['data']['is_away'] == 'True' and data['data']['days'] == 10


def test_timer(client):
    login(client)

    payload = {'is_closed': True, 'time': 10}
    rv = client.post('/timer/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == 'Timer successfully recorded/retrieved'

    request = client.get("/timer/")
    assert request.status_code == 200
    data = json.loads(request.data)
    assert data['data']['is_closed'] == 'True' and data['data']['time'] == 10


def test_stock(client):
    login(client)

    payload = {'product_name': 'aliment1', 'quantity': 1, 'product_expiration_date': "2022-01-31 13:37:24", 'shelf_number': 3}
    rv = client.post('/stock/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert res["status"] == 'Stock successfully recorded/retrieved'

    request = client.get("/stock/")
    assert request.status_code == 200
    data = json.loads(request.data)
    ok = False
    for product in data['data']:
        if product['product_name'] == 'aliment1' and product['quantity'] == 1:
            ok = True
    assert ok is True


def test_expired(client):
    login(client)

    payload = {'product_name': 'aliment11', 'quantity': 1, 'product_expiration_date': "2022-02-03 13:37:24", 'shelf_number': 3}
    rv = client.post('/stock/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert res["status"] == 'Stock successfully recorded/retrieved'

    request = client.get("/stock/")
    assert request.status_code == 200
    data = json.loads(request.data)
    assert in_stock(data, 'aliment11', 1) is True

    payload = {'product_name': 'aliment2', 'quantity': 2, 'product_expiration_date': "2022-03-31 13:37:24", 'shelf_number': 3}
    rv = client.post('/stock/', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert res["status"] == 'Stock successfully recorded/retrieved'

    request = client.get("/stock/")
    assert request.status_code == 200
    data = json.loads(request.data)
    assert in_stock(data, 'aliment2', 2) is True

    request = client.get("/stock/expired")
    assert request.status_code == 200

    data = json.loads(request.data)
    # expira in urmatoarele 3 zile
    assert in_stock(data, 'aliment11', 1) is True
    # nu expira in urmatoarele 3 zile
    assert in_stock(data, 'aliment2', 2) is False
