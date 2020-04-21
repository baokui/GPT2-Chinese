from flask import Flask
from  gevent.pywsgi import WSGIServer
from gevent import monkey
import time
import sys
port = sys.argv[1]
monkey.patch_all()
app = Flask(__name__)
@app.route('/')
def hello_world():
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec

    T0 = '-'.join([str(hour), '时', str(minute), '分', str(second), '秒'])
    time.sleep(10)

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec

    T1 = '-'.join([str(hour), '时', str(minute), '分', str(second), '秒'])
    return 'Hello World!'+T0+'->'+T1

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()