from functools import reduce


class EmployeeDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.employee_name = data.get('employee_name')
        self.hours_per_day = data.get('hours_per_day')
        self.available_days = data.get('available_days')

        # opts
        if data.get('group_skills') is not None:
            self.group_skills = data.get('group_skills')

        if data.get('group_skills_id') is not None:
            self.group_skills_id = data.get('group_skills_id')

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "employee_name": self.employee_name,
            "hours_per_day": self.hours_per_day,
            "available_days": self.available_days,

        }

        if hasattr(self, 'group_skills'):
            output['group_skills'] = self.group_skills

        if hasattr(self, 'group_skills_id'):
            output['group_skills_id'] = self.group_skills_id

        return output

    def set_skill_set(self, skill_set):
        self.skill_set = skill_set


class EmployeeListDTO:
    def __init__(self, data):
        self.list = [EmployeeDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]

    @property
    def get_days(self):
        arr = [item.available_days.split(',') for item in self.list]
        if len(arr) == 0:
            return None
        output = reduce(lambda a, b: a+b, arr)

        return ', '.join(list(dict.fromkeys(output)))


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
