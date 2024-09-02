from .employee_repository import EmployeeRepository
from .skill_repository import SkillRepository
from .employee_skill_repository import EmployeeSkillRepository

class UnitOfWork:
    def __init__(self, make_db_conn):
        self.connection = make_db_conn()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with_rollback = True if exc_type is not None else False
        self._close(with_rollback)

    def _close(self, with_rollback: bool) -> None:
        if with_rollback:
            self.rollback()
        else:
            self.commit()

        self.connection.close()
    
    @property
    def employee_repository(self) -> EmployeeRepository:
        return EmployeeRepository(self.connection)
    
    @property
    def skill_repository(self) -> SkillRepository:
        return SkillRepository(self.connection)
    
    @property
    def employee_repository(self) -> EmployeeSkillRepository:
        return EmployeeSkillRepository(self.connection)