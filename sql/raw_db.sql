CREATE TABLE employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name VARCHAR(100),
    hours_per_day INT,
    available_days VARCHAR(50) -- Lista de días en un formato (ejemplo: '1, 3, 5')
);

CREATE TABLE skill (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name VARCHAR(50)
);

CREATE TABLE employee_skill (
    employee_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id),
    PRIMARY KEY (employee_id, skill_id)
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100),
    due_date DATE,
    time_use INTEGER,
    is_assignment INTEGER
);

CREATE TABLE task_skill_set (
    task_id INTEGER,
    skill_id INTEGER,
    FOREIGN KEY (task_id) REFERENCES task(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id),
    PRIMARY KEY (task_id, skill_id)
);

CREATE TABLE assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    task_id INTEGER,
    date_assignment DATE,
    hour_assignment INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (task_id) REFERENCES task(id)
);

INSERT INTO
    "employee" (
        "employee_name",
        "hours_per_day",
        "available_days"
    )
VALUES
    ('Sam', '8', '1,2,3,4,5'),
    ('John', '4', '1,2,3,4,5'),
    ('Rebecca', '8', '1,3,5'),
    ('Sebastian', '4', '1,2,3,4,5');

INSERT INTO
    "skill" ("skill_name")
VALUES
    ('programacion'),
    ('diseño'),
    ('analisis'),
    ('coordinacion');

INSERT INTO
    "employee_skill" ("employee_id", "skill_id")
VALUES
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4');

CREATE VIEW calendar_availability AS WITH stats as (
    SELECT
        assignment.employee_id,
        count(assignment.id) as amount_task,
        sum(assignment.hour_assignment) as hours_spent,
        assignment.date_assignment
    FROM
        assignment
    GROUP BY
        assignment.date_assignment,
        assignment.employee_id
)
SELECT
    employee.*,
    stats.date_assignment,
    COALESCE(stats.amount_task, 0) AS amount_task,
    COALESCE(stats.hours_spent, 0) AS hours_spent,
    employee.hours_per_day - COALESCE(stats.hours_spent, 0) AS hours_remaining
FROM
    employee
    LEFT JOIN stats ON stats.employee_id = employee.id
ORDER BY
    stats.date_assignment ASC;