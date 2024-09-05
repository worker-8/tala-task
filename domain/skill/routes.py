from flask import Blueprint
from . import controller

def add_routes(parent: Blueprint) -> None:
    router = Blueprint("skill", __name__, "/skill")

    router.add_url_rule('/skill', view_func=controller.find_skill)
    router.add_url_rule('/skill', view_func=controller.create_skill, methods=["POST"])
    router.add_url_rule("/skill/csv", view_func=controller.upload_csv, methods=["GET", "POST"])

    parent.register_blueprint(router)