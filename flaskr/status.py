from db import get_db


def get_status():
    temperature = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    rgb = get_db().execute(
        'SELECT id, timestamp, red, green, blue'
        ' FROM rgb'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    timer = get_db().execute(
        'SELECT id, timestamp, is_closed, time'
        ' FROM timer'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    holiday = get_db().execute(
        'SELECT id, timestamp, is_away, days'
        ' FROM holiday'
        ' ORDER BY timestamp DESC'
    ).fetchone()

    stock = get_db().execute(
        'SELECT id, product_name, quantity, product_expiration_date, shelf_number'
        ' FROM stock'
        ' ORDER BY product_expiration_date DESC'
    ).fetchone()

    if temperature is None:
        return {'status': 'Please set a value for temperature'}

    if rgb is None:
        return {'status': 'Please select your RGB code'}

    if timer is None:
        return {'status': 'Please tell when to close the door'}

    if holiday is None:
        return {'status': 'Are you on holiday or not?'}

    if stock is None:
        return {'status': 'GOOOOOOOOOOL!!!'}

    return {
        'data': {
            'temperature': temperature['value'],
            'rgb': {
                'last_changed': rgb['timestamp'],
                'red': rgb['red'], 'green': rgb['green'], 'blue': rgb['blue']
            },
            'timer': {
                'last_changed': timer['timestamp'],
                'is_closed': timer['is_closed'],
                'time': timer['time']
            },
            'holiday': {
                'last_changed': holiday['timestamp'],
                'is_away': holiday['is_away'],
                'days': holiday['days']
            },
            'stock': {
                'product_name': stock['product_name'],
                'quantity': stock['quantity'],
                'product_expiration_date': stock['product_expiration_date'],
                'shelf_number': stock['shelf_number']
            }
        }
    }
def get_timer():
    timer = get_db().execute(
        'SELECT id, timestamp, is_closed, time'
        ' FROM timer'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return timer['is_closed'], timer['time']

def get_temp():
    temp = get_db().execute(
        'SELECT id, timestamp, value'
        ' FROM temperature'
        ' ORDER BY timestamp DESC'
    ).fetchone()
    return temp['value']
