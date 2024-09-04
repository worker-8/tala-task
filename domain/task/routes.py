from flask import Blueprint
from . import controller


def add_routes(parent: Blueprint) -> None:
    router = Blueprint("task", __name__, "/task")

    router.add_url_rule("/task", view_func=controller.find_task)
    router.add_url_rule("/task", view_func=controller.create_task, methods=["POST"])
    router.add_url_rule("/task/assignment",
                        view_func=controller.assignment_task)

    parent.register_blueprint(router)
