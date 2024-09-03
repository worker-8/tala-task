class EmployeeRepository:
    def __init__(self, connection):
        self.connection = connection
    
    def find(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM employee"
        cursor.execute(query, [])

        return cursor.fetchall()
