from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.employee.employee_dto import EmployeeDTO


class EmployeeRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: EmployeeDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        query = f"INSERT INTO employee({fields}) VALUES({values}) RETURNING *"
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    def find(self):
        builder = QueryBuilder()

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM employee
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
