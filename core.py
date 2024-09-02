from flask import Flask

class Wrapper:
    def __init__(self, app: Flask):
        self.app = app

def create_app() -> Wrapper:
    app = Flask(__name__)
    return Wrapper(app)