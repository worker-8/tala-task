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
        builder.add(payload.is_assignment, 'is_assignment = ?')

        cursor = self.connection.cursor()
        query = f"""
            SELECT *
            FROM task
            {builder.where}
            """
        cursor.execute(query, builder.params)

        return cursor.fetchall()

    def findWithGroupConcatOnSkillName(self, payload: TaskDTO):
        builder = QueryBuilder()

        builder.add(payload.id, 'task.id = ?')
        builder.add(payload.is_assignment, 'task.is_assignment = ?')
        builder.like(payload.title, 'LOWER(task.title) LIKE LOWER(?)',
                     lambda x: "%{}%".format(x))

        cursor = self.connection.cursor()
        query = f"""
            SELECT task.*,
                    group_concat(skill.skill_name) as group_skills,
                    group_concat(skill.id) as group_skills_id
            FROM task
            INNER JOIN task_skill_set ON task.id = task_skill_set.task_id
            INNER JOIN skill ON task_skill_set.skill_id = skill.id
            {builder.where}
            GROUP BY task.id;
        """
        cursor.execute(query, builder.params)

        return cursor.fetchall()
