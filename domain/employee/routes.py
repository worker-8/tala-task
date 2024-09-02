from flask import Blueprint
from . import controller

def add_routes(parent: Blueprint) -> None:
    router = Blueprint("employee", __name__, "/employee")

    router.add_url_rule("/employee", view_func=controller.fetch_employee)

    parent.register_blueprint(router)