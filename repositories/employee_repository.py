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
    
    def findWithGroupConcatOnSkillName(self, skill_set):
        cursor = self.connection.cursor()
        query = f"""
            WITH employee_pluss AS (SELECT 
                employee.*,
                group_concat(skill.skill_name) as group_skills,
                group_concat(skill.id) as group_skills_id
            FROM employee
            INNER JOIN employee_skill ON employee.id = employee_skill.employee_id
            INNER JOIN skill ON employee_skill.skill_id = skill.id
            GROUP BY employee.id)
            SELECT * FROM employee_pluss
            WHERE group_skills_id LIKE '%{skill_set}%'
            """
        cursor.execute(query, [])

        return cursor.fetchall()
