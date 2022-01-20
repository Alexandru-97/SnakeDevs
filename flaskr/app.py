import os
from flask import Flask
from threading import Thread
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import eventlet
import json
import time
import db
import auth
import environment
import status_api
import status
import rgb
import timer
import holiday
import stock
import temperature

eventlet.monkey_patch()

app = None
mqtt = None
socketio = None
thread = None

test_config = None


def create_app():
    global app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

    @app.route('/')
    def hello_world():
        global thread
        if thread is None:
            thread = Thread(target=background_thread)
            thread.daemon = True
            thread.start()
        return 'Hello User, not World!'

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(status_api.bp)
    app.register_blueprint(rgb.bp)
    app.register_blueprint(timer.bp)
    app.register_blueprint(holiday.bp)
    app.register_blueprint(stock.bp)
    app.register_blueprint(temperature.bp)

    return app


def create_mqtt_app():

    # Setup connection to mqtt broker
    app.config['MQTT_BROKER_URL'] = 'localhost'  # use the free broker from HIVEMQ
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

    global mqtt
    mqtt = Mqtt(app)
    global socketio
    socketio = SocketIO(app, async_mode="eventlet")

    return mqtt


def background_thread():
    count = 0
    while True:
        time.sleep(1)
        with app.app_context():
            message = json.dumps(status.get_status(), default=str)
        # Publish
        mqtt.publish('python/mqtt', message)


def run_socketio_app():
    create_app()
    create_mqtt_app()
    socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

if __name__ == '__main__':
    run_socketio_app()
