# https://blog.miguelgrinberg.com/post/add-a-websocket-route-to-your-flask-2-x-application
# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
# python.exe -m flask run  --host=0.0.0.0 --port=7788
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def index():
    return render_template('index.html')


@sock.route('/')
def echo(sock):
    while True:
        data = sock.receive()
        print(data)
        # sock.send(data[::-1])
        sock.send(data)