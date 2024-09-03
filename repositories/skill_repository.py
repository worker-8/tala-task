from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.skill.skill_dto import SkillDTO


class SkillRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: SkillDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        query = f"INSERT INTO skill({fields}) VALUES({values}) RETURNING *"
        cursor = self.connection.cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    def find(self, payload: SkillDTO):
        builder = QueryBuilder()
        builder.add(payload.id, "id = ?")

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM skill
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
