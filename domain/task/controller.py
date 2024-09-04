from flask import request
from repositories import create_uow

from .task_dto import TaskDTO, TaskSkillSetDTO
from domain.skill.skill_dto import SkillDTO, SkillListDTO


def find_task():
    return {"status": True}


def create_task():
    payload_task = TaskDTO(request.json)
    list_of_skill = request.json.get("skill_set")

    with create_uow() as uow:
        if list_of_skill is None:
            return ({
                'status': False,
                'message': 'It is not possible to create a task without at least one required Skill'}, 401)
        nw_task = uow.task_repository.create(payload_task)

        for skill in list_of_skill.split(','):
            _merge_task_skill(uow=uow, task_id=nw_task['id'], skill_id=skill)

        tss_dto = TaskSkillSetDTO({"task_id": nw_task['id']})
        skill_set = uow.task_skill_set_repository.findMetaData(payload=tss_dto)

        output = TaskDTO(dict(nw_task))
        output.set_skill_set(SkillListDTO(skill_set).to_json)
        uow.rollback()
        return {"status": True, "task": output.to_json}


def assignment_task():
    return {"status": True}


def _merge_task_skill(uow: create_uow, task_id: int, skill_id: int):
    skillDTO = SkillDTO(data={})
    skillDTO.id = skill_id
    skill = uow.skill_repository.find(payload=skillDTO)
    
    if len(skill) == 0:
        print(f'Skill ID {skill_id} does not exist')
        return False
    
    tss_dto = TaskSkillSetDTO({"task_id": task_id, "skill_id": skill_id})
    uow.task_skill_set_repository.create(data=tss_dto)

    return True
