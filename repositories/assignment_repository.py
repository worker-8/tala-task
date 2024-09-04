from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.task.task_dto import AssignmentDTO


class AssignmentRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: AssignmentDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        query = f"INSERT INTO assignment({fields}) VALUES({
            values}) RETURNING *"
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    def find(self, payload: AssignmentDTO):
        builder = QueryBuilder()

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM assignment
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
