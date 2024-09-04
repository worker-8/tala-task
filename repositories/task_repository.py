from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.task.task_dto import TaskDTO


class TaskRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: TaskDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        query = f"INSERT INTO task({fields}) VALUES({values}) RETURNING *"
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    def find(self, payload: TaskDTO):
        builder = QueryBuilder()

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM task
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
