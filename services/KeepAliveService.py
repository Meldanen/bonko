from threading import Thread

from flask import Flask
from waitress import serve

app = Flask(__name__)


@app.route('/')
def home():
    return "I'm alive"


def run():
    serve(app, host="0.0.0.0", port=8080)
    # app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
