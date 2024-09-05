from flask import request
from repositories import create_uow
from helpers.csv import read_csv, form_upload

from .task_dto import TaskDTO, TaskSkillSetDTO, TaskListDTO, AssignmentDTO
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

    nw_task = _create_task_helper(task=payload_task, list_of_skill=list_of_skill)
    return {"status": True, "tasks": nw_task}

def upload_csv():
    if request.method == "POST":
        f = request.files.get('csv')
        tasks = read_csv(f)
        output = []

        for task in tasks:
            t_dto = TaskDTO(data={})
            t_dto.title = task[0]
            t_dto.due_date = task[1]
            t_dto.time_use = task[2]

            nw_task = _create_task_helper(task=t_dto, list_of_skill=task[3])
            output.append(nw_task)

        return {"status": True, "tasks": output}
    else:
        return form_upload(title='Upload tasks')


def _create_task_helper(task: TaskDTO, list_of_skill):
    with create_uow() as uow:
        if list_of_skill is None:
            return ({
                'status': False,
                'message': 'It is not possible to create a task without at least one required Skill'}, 401)
        nw_task = uow.task_repository.create(task)

        for skill in list_of_skill.split(','):
            _merge_task_skill(uow=uow, task_id=nw_task['id'], skill_id=skill)

        tss_dto = TaskSkillSetDTO({"task_id": nw_task['id']})
        skill_set = uow.task_skill_set_repository.findMetaData(payload=tss_dto)

        output = TaskDTO(dict(nw_task))
        output.set_skill_set(SkillListDTO(skill_set).to_json)
        return output.to_json


def assignment_task():
    # Control assignment
    task_assign = []
    task_not_assign = []
    with create_uow() as uow:
        # 0. task list
        tasks = _task_list(uow=uow)
        if len(tasks.list) == 0:
            return {"status": True, "message": "There are no tasks available for assignment"}

        employees = None
        # 1. find user By skill
        for task in tasks.list:
            employees = _employee_list(uow=uow, skill_set=task.group_skills_id)
            employees.get_days
            if len(employees.list) == 0:
                print(f'task {task.title} not has staff')
                task_not_assign.append(task.to_json)
                continue
            employees.get_days
            # 1.1 find calendar
            calendar = _get_calendar(
                uow=uow, due_date=task.due_date, available_days=employees.get_days)
            # 2. get callendar By User AND days capacity
            pick_employee, date_assignment = _pick_employee(
                uow=uow, calendar=calendar, employees=employees.list, time_use=task.time_use)

            # 3. assignment task
            assignment_dto = AssignmentDTO(data={
                "employee_id": pick_employee,
                "task_id": task.id,
                "date_assignment": date_assignment,
                "hour_assignment": task.time_use
            })

            uow.assignment_repository.create(data=assignment_dto)
            task.is_assignment = 1
            uow.task_repository.update(data=task)
            task_assign.append(task.to_json)

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


def _get_calendar(uow: create_uow, due_date, available_days):
    calendar = uow.assignment_repository.calendar(
        due_date=due_date, available_days=available_days)
    return [dict(item) for item in calendar]


def _pick_employee(uow: create_uow, calendar, employees, time_use):
    pick_employee_id = None
    date_assignment = None
    loop = 0
    for d in calendar:
        loop += 1
        date_assignment = d.get('possible_date')
        week_day = str(d.get('week_day'))
        employees_id = list()
        employees_id_str = ''

        for employee in employees:
            if week_day in employee.available_days:
                employees_id.append(employee.id)

        employees_id_str = ", ".join(str(v) for v in employees_id)

        rs = uow.employee_repository.calendarAvailability(
            date_assignment=date_assignment, employees_id=employees_id_str)

        candidates = [dict(item) for item in rs]

        if len(candidates) == 0:
            pick_employee_id = employees_id[0]
            break

        if len(candidates) < len(employees_id):
            pick_employee_id = employees_id[len(candidates)]
            break

        for candidate in candidates:
            if candidate.get('hours_remaining') >= time_use:
                pick_employee_id = candidate.get('id')
                break

        if pick_employee_id is not None and date_assignment is not None:
            break

    return pick_employee_id, date_assignment


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
