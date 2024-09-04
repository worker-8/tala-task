class SkillDTO:
    def __init__(self, data):
        self.id = data.get("id")
        self.skill_name = data.get("skill_name")

    @property
    def to_json(self):
        return {
            "id": self.id,
            "skill_name": self.skill_name
        }


class SkillListDTO:
    def __init__(self, data):
        self.list = [SkillDTO(dict(item)) for item in data]

    @property
    def to_json(self):
        return [item.to_json for item in self.list]
