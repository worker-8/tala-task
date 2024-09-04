from flask import request
from repositories import create_uow

from .task_dto import TaskDTO, TaskSkillSetDTO, TaskListDTO
from domain.skill.skill_dto import SkillDTO, SkillListDTO
from domain.employee.employee_dto import EmployeeDTO, EmployeeListDTO


def find_task():
    payload_task = TaskDTO(data={})
    with create_uow() as uow:
        rs = uow.task_repository.findWithGroupConcatOnSkillName(
            payload=payload_task)
        list = TaskListDTO(data=rs).to_json
        return {"status": True, "list": list}


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
        return {"status": True, "task": output.to_json}


def assignment_task():
    # Control assignment
    task_assign = []
    task_not_assign = []
    with create_uow() as uow:
        # 0. task list
        tasks = _task_list(uow=uow)

        employees = None
        # 1. find user By skill
        for task in tasks.list:
            employees = _employee_list(uow=uow, skill_set=task.group_skills_id)

            if len(employees.list) == 0:
                print(f'task {task.title} not has staff')
                task_not_assign.append(task.to_json)
                continue
            task_assign.append(task.to_json)
        # 2. get callendar By User AND days capacity
        # 3. assignment task
        return {"status": True, "task_not_assign": task_not_assign, "task_assign": task_assign}


def _task_list(uow: create_uow):
    # ONLY TASK IS_ASSIGNED FALSE (0)
    rs = uow.task_repository.findWithGroupConcatOnSkillName(
        payload=TaskDTO({}))
    return TaskListDTO(rs)


def _employee_list(uow: create_uow, skill_set):
    rs = uow.employee_repository.findWithGroupConcatOnSkillName(
        skill_set=skill_set)
    return EmployeeListDTO(rs)


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
