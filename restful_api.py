from flask import Flask,g
from data_base import RedisClient
app = Flask(__name__)
def get_conn():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis
@app.route('/')
def index():
    return '<h2> Welcome to Proxy Pool stytem</h2>'
@app.route('/random')
def get_proxy():
    conn = get_conn()
    return conn.radom()
@app.route('/count')
def count():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()