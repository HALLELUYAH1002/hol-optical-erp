from datetime import datetime


def now_str():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
