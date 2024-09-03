from flask import request
from repositories import create_uow

def fetch_employee():
    with create_uow() as uow:
        employees = uow.employee_repository.find()
        for employee in employees:
            print(employee['employee_name'])
        
        return {"status":True}