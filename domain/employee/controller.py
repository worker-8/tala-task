from flask import request
from repositories import create_uow

from .employee_dto import EmployeeListDTO, EmployeeDTO, EmployeeSkillDTO
from domain.skill.skill_dto import SkillDTO, SkillListDTO


def fetch_employee():
    with create_uow() as uow:
        employees = uow.employee_repository.find()
        list = EmployeeListDTO(employees)
        for employee in list.list:
            esDTO = EmployeeSkillDTO({"employee_id": employee.id})
            skill_set = uow.employee_skill_repository.findMetaData(payload=esDTO)
            employee.set_skill_set(SkillListDTO(skill_set).to_json)  

        return {"status": True, "employees": list.to_json}


def create_employee():
    payload_user = EmployeeDTO(request.json)
    list_of_skill = request.json.get("skill_set")
    with create_uow() as uow:
        # TODO: verify if the user is there.
        nw_employee = uow.employee_repository.create(payload_user)
        if list_of_skill is None:
            return {"status": True, "payload": EmployeeDTO(dict(nw_employee)).to_json}

        for skill in list_of_skill.split(','):
            _merge_employee_skill(
                uow=uow, employee_id=nw_employee['id'], skill_id=int(skill))
        
        esDTO = EmployeeSkillDTO({"employee_id": nw_employee['id']})
        skill_set = uow.employee_skill_repository.findMetaData(payload=esDTO)

        output = EmployeeDTO(dict(nw_employee))
        output.set_skill_set(SkillListDTO(skill_set).to_json)


        return {"status": True, "payload": output.to_json}


def _merge_employee_skill(uow: create_uow, employee_id: int, skill_id: int):
    skillDTO = SkillDTO(data={})
    skillDTO.id = skill_id
    skill = uow.skill_repository.find(payload=skillDTO)
    if len(skill) == 0:
        print(f'Skill ID {skill_id} does not exist')
        return False

    esDTO = EmployeeSkillDTO(
        data={"employee_id": employee_id, "skill_id": skill_id})
    uow.employee_skill_repository.create(data=esDTO)

    return True
