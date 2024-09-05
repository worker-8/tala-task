from flask import request
from repositories import create_uow
from helpers.csv import read_csv, form_upload

from .employee_dto import EmployeeListDTO, EmployeeDTO, EmployeeSkillDTO
from domain.skill.skill_dto import SkillDTO, SkillListDTO


def fetch_employee():
    with create_uow() as uow:
        employees = uow.employee_repository.find()
        list = EmployeeListDTO(employees)
        for employee in list.list:
            esDTO = EmployeeSkillDTO({"employee_id": employee.id})
            skill_set = uow.employee_skill_repository.findMetaData(
                payload=esDTO)
            employee.set_skill_set(SkillListDTO(skill_set).to_json)

        return {"status": True, "employees": list.to_json}


def create_employee():
    payload_user = EmployeeDTO(request.json)
    list_of_skill = request.json.get("skill_set")

    nw_employee = _create_employee_helper(
        payload_user, list_of_skill=list_of_skill)
    
    if 'msg_error' in nw_employee:
        return ({"status": False, "employee": nw_employee}, 401)

    return {"status": True, "employee": nw_employee}


def upload_csv():
    if request.method == "POST":
        f = request.files.get('csv')
        employees = read_csv(f)
        output = []

        for employee in employees:
            e_dto = EmployeeDTO(data={})
            e_dto.employee_name = employee[0]
            e_dto.hours_per_day = employee[1]
            e_dto.available_days = employee[2]
            nw_employee = _create_employee_helper(employee=e_dto, list_of_skill=employee[3])
            output.append(nw_employee)
        return {"status": True, "employees": output}
    else:
        return form_upload(title='Upload Employees')


def _create_employee_helper(employee: EmployeeDTO, list_of_skill):
    with create_uow() as uow:
        if employee.is_valid == False:
            return employee.to_json
        
        if list_of_skill is None or len(list_of_skill) == 0:
            employee.msg_error = [
                'It is not possible to create a employee without at least one required Skill']
            return employee.to_json
        
        return {"test":True}
        # TODO: verify if the user is there.
        nw_employee = uow.employee_repository.create(employee)

        for skill in list_of_skill.split(','):
            _merge_employee_skill(
                uow=uow, employee_id=nw_employee['id'], skill_id=int(skill))

        esDTO = EmployeeSkillDTO({"employee_id": nw_employee['id']})
        skill_set = uow.employee_skill_repository.findMetaData(payload=esDTO)

        output = EmployeeDTO(dict(nw_employee))
        output.set_skill_set(SkillListDTO(skill_set).to_json)

        return output.to_json


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
