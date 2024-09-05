from flask import Blueprint
from . import controller


def add_routes(parent: Blueprint) -> None:
    router = Blueprint("task", __name__, "/task")

    router.add_url_rule("/task", view_func=controller.find_task)
    router.add_url_rule("/task", view_func=controller.create_task, methods=["POST"])
    router.add_url_rule("/task/report", view_func=controller.report)
    router.add_url_rule("/task/assignment",
                        view_func=controller.assignment_task)
    router.add_url_rule("/task/csv", view_func=controller.upload_csv, methods=["GET", "POST"])

    parent.register_blueprint(router)
