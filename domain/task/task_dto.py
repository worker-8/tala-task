class TaskDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.title = data.get("title")
        self.due_date = data.get("due_date")
        self.time_use = data.get("time_use")

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "time_use": self.time_use
        }

        if hasattr(self, 'skill_set'):
            output['skill_set'] = self.skill_set

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
