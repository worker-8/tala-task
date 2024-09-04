class EmployeeDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.employee_name = data.get('employee_name')
        self.hours_per_day = data.get('hours_per_day')
        self.available_days = data.get('available_days')

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "employee_name": self.employee_name,
            "hours_per_day": self.hours_per_day,
            "available_days": self.available_days,
        }

        if hasattr(self, 'skill_set'):
            output['skill_set'] = self.skill_set

        return output

    def set_skill_set(self, skill_set):
        self.skill_set = skill_set


class EmployeeListDTO:
    def __init__(self, data):
        self.list = [EmployeeDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]


class EmployeeSkillDTO:
    def __init__(self, data):
        self.employee_id = data.get('employee_id')
        self.skill_id = data.get('skill_id')

    @property
    def to_json(self):
        return {
            "employee_id": self.employee_id,
            "skill_id": self.skill_id
        }
