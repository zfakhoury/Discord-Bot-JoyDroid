from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "JoyDroid on duty"


def run():
    app.run(host='0.0.0.0', port=8080)


def revive():
    operation = Thread(target=run)
    operation.start()
