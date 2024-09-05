import os
from flask import Blueprint
from helpers.plugins import register_domains
from helpers.middlewares import register_middlewares
from werkzeug.utils import secure_filename

from core import create_app

app = create_app().app
v1_endpoints = Blueprint("v1", __name__, url_prefix="/api/v1")

UPLOAD_FOLDER = './upload/'
ALLOWED_EXTENSIONS = {'csv'}

register_middlewares(app)
register_domains(v1_endpoints)

app.register_blueprint(v1_endpoints)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == "__main__":
    app.run(debug=True)