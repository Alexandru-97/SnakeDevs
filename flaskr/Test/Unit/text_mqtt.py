import pytest
import json
from app import create_mqtt_app, create_app
from paho.mqtt.client import MQTT_ERR_SUCCESS


# python -m pytest -v Test/Unit/test_mqtt.py


@pytest.fixture()
def client():
    create_app()
    local_mqtt_app = create_mqtt_app()
    # client = local_mqtt_app.test_client()

    yield local_mqtt_app


def on_publish(client, userdata, result):
    print("data published")
    pass


def test_mqtt_publishing(client):
    payload = "Test data"
    client.on_publish = on_publish
    ret = client.publish("python/mqtt", payload)
    assert ret[0] == MQTT_ERR_SUCCESS