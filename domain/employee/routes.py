from flask import Blueprint
from . import controller

def add_routes(parent: Blueprint) -> None:
    router = Blueprint("employee", __name__, "/employee")

    router.add_url_rule("/employee", view_func=controller.fetch_employee)
    router.add_url_rule("/employee", view_func=controller.create_employee, methods=["POST"])

    parent.register_blueprint(router)