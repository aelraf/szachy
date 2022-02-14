# -*- coding: utf-8 -*-
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Chess with Python Flask'


@app.route('/api')
def main():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)




