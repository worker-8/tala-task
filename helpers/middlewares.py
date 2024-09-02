from flask import Flask

def check_headers():
    # in case if you want add api key or similar.
    pass

def register_middlewares(app: Flask):
    app.before_request(check_headers)