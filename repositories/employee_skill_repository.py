from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.employee.employee_dto import EmployeeSkillDTO


class EmployeeSkillRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: EmployeeSkillDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        query = f"INSERT INTO employee_skill({fields}) VALUES({
            values}) RETURNING *"
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    def find(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM employee_skill"
        cursor.execute(query, [])

        return cursor.fetchall()

    def findMetaData(self, payload: EmployeeSkillDTO):
        builder = QueryBuilder()
        builder.add(payload.employee_id, "employee_skill.employee_id = ?")
        builder.add(payload.skill_id, "employee_skill.skill_id = ?")

        cursor = self.connection.cursor()
        query = f"""
            SELECT skill.*
            FROM employee_skill
            INNER JOIN skill ON employee_skill.skill_id = skill.id
            {builder.where}
        """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
