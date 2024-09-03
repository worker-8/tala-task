from flask import request
from repositories import create_uow

from .skill_dto import SkillListDTO, SkillDTO

def find_skill():
    with create_uow() as uow:
        skills = uow.skill_repository.find(SkillDTO(data={}))
        list = SkillListDTO(skills)
        return {"status": True, "skills": list.to_json}

def create_skill():
    payload = SkillDTO(request.json)
    with create_uow() as uow:
        #TODO: verify if the skill is there.
        nw_skill = uow.skill_repository.create(payload)
        return {"status": True, "payload": SkillDTO(dict(nw_skill)).to_json}