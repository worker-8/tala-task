class EmployeeDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.employee_name = data.get('employee_name')
        self.hours_per_day = data.get('hours_per_day')
        self.available_days = data.get('available_days')

    @property
    def to_json(self):
        return {
            "id": self.id,
            "employee_name": self.employee_name,
            "hours_per_day": self.hours_per_day,
            "available_days": self.available_days     
        }

class EmployeeListDTO:
    def __init__(self, data):
        self.list = [EmployeeDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]
