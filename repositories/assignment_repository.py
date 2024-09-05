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
    
    def calendar(self, due_date, available_days):
        cursor = self.connection.cursor()
        query = f"""
            WITH calendar AS (
                WITH RECURSIVE dates(date) AS (
                VALUES(date('now'))
                UNION ALL
                SELECT date(date, '+1 days')
                FROM dates
                WHERE date < ?
                )
            SELECT date AS possible_date, strftime('%w', date) +1 AS week_day FROM dates)
            SELECT * FROM calendar
            WHERE week_day IN ({available_days});
        """

        cursor.execute(query, [due_date])

        return cursor.fetchall()
    
    def report(self):
        cursor = self.connection.cursor()
        query = f"""
                SELECT * 
                FROM calendar_availability
            """
        cursor.execute(query, [])
        
        return cursor.fetchall()
