class SkillRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def find(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM skill"
        cursor.execute(query, [])

        return cursor.fetchall()