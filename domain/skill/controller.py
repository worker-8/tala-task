from flask import request
from repositories import create_uow
from helpers.csv import read_csv, form_upload

from .skill_dto import SkillListDTO, SkillDTO


def find_skill():
    with create_uow() as uow:
        skills = uow.skill_repository.find(SkillDTO(data={}))
        list = SkillListDTO(skills)
        return {"status": True, "skills": list.to_json}


def create_skill():
    payload = SkillDTO(request.json)
    nw_skill = _create_skill_helper(skill=payload)
    return {"status": True, "skill": nw_skill}


def upload_csv():
    if request.method == "POST":
        f = request.files.get('csv')
        skills = read_csv(f)
        output = []

        for skill in skills:
            s_dto = SkillDTO(data={})
            s_dto.skill_name = skill[0]

            nw_skill = _create_skill_helper(skill=s_dto)
            output.append(nw_skill)

        return {"status": True, "skills": output}
    else:
        return form_upload(title='Upload skills')


def _create_skill_helper(skill: SkillDTO):
    with create_uow() as uow:
        if skill.is_valid == False:
            return skill.to_json
        # TODO: verify if the skill is there.
        nw_skill = uow.skill_repository.create(skill)
        return SkillDTO(dict(nw_skill)).to_json
