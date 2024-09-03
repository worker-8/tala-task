from helpers.query_builder import QueryBuilder
from helpers.sql import create_fields_values_params

from domain.task.task_dto import TaskSkillSetDTO


class TaskSkillSetRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, data: TaskSkillSetDTO):
        fields, values, params = create_fields_values_params(data.__dict__)
        print(fields, values, params)
        query = f"""
            INSERT INTO task_skill_set({fields}) 
            VALUES({values}) 
            RETURNING *
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        
        return cursor.fetchone()

    def find(self, payload: TaskSkillSetDTO):
        builder = QueryBuilder()

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM task_skill_set
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
    
    def findMetaData(self, payload: TaskSkillSetDTO):
        builder = QueryBuilder()
        builder.add(payload.task_id, "task_skill_set.task_id = ?")

        cursor = self.connection.cursor()
        query = f"""
            SELECT skill.*
            FROM task_skill_set
            INNER JOIN skill ON task_skill_set.skill_id = skill.id
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
