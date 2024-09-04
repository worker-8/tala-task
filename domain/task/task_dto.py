class TaskDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.title = data.get("title")
        self.due_date = data.get("due_date")
        self.time_use = data.get("time_use")
        self.is_assignment = str(data.get("is_assignment", "0"))

        # opts
        if data.get('group_skills') is not None:
            self.group_skills = data.get('group_skills')
        
        if data.get('group_skills_id') is not None:
            self.group_skills_id = data.get('group_skills_id')

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "time_use": self.time_use,
            "is_assignment": self.is_assignment,
        }

        if hasattr(self, 'group_skills'):
            output['group_skills'] = self.group_skills
        
        if hasattr(self, 'group_skills_id'):
            output['group_skills_id'] = self.group_skills_id

        return output

    def set_skill_set(self, skill_set):
        self.skill_set = skill_set


class TaskListDTO:
    def __init__(self, data):
        self.list = [TaskDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]


class TaskSkillSetDTO:
    def __init__(self, data):
        self.task_id = data.get("task_id")
        self.skill_id = data.get("skill_id")

    @property
    def to_json(self):
        return {
            "task_id": self.task_id,
            "skill_id": self.skill_id
        }


class TaskSkillListDTO:
    def __init__(self, data):
        self.list = [TaskSkillSetDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]


class AssignmentDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.employee_id = data.get("employee_id")
        self.task_id = data.get("task_id")
        self.date_assignment = data.get("date_assignment")
        self.hour_assignment = data.get("hour_assignment")

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "employee_id": self.employee_id,
            "task_id": self.task_id,
            "date_assignment": self.date_assignment,
            "hour_assignment": self.hour_assignment
        }

        return output
