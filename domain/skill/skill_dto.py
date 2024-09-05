class SkillDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.skill_name = data.get("skill_name", '')

    @property
    def to_json(self):
        output = {
            "id": self.id,
            "skill_name": self.skill_name
        }

        if hasattr(self, 'msg_error'):
            output['msg_error'] = self.msg_error

        return output

    @property
    def is_valid(self):
        valid = True
        self.msg_error = []

        if len(self.skill_name) == 0:
            valid = False
            self.msg_error.append('Must have a skill name')

        if valid:
            delattr(self, 'msg_error')

        return valid


class SkillListDTO:
    def __init__(self, data):
        self.list = [SkillDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]
