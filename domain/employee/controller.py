from flask import request
from repositories import create_uow

from .employee_dto import EmployeeListDTO, EmployeeDTO

def fetch_employee():
    with create_uow() as uow:
        employees = uow.employee_repository.find()
        list = EmployeeListDTO(employees)
        return {"status":True, "employees": list.to_json}

def create_employee():
    payload = EmployeeDTO(request.json)
    with create_uow() as uow:
        # TODO: verify if the user is there.
        nw_employee = uow.employee_repository.create(payload)
        return {"status": True, "payload": EmployeeDTO(dict(nw_employee)).__dict__}