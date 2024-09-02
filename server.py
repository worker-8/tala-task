from flask import Blueprint
from helpers.plugins import register_domains
from helpers.middlewares import register_middlewares

from core import create_app

app = create_app().app
v1_endpoints = Blueprint("v1", __name__, url_prefix="/api/v1")

register_middlewares(app)
register_domains(v1_endpoints)

app.register_blueprint(v1_endpoints)

if __name__ == "__main__":
    app.run(debug=True)