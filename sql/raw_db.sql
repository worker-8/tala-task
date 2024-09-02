CREATE TABLE employee (
    id INT PRIMARY KEY,
    employee_name VARCHAR(100),
    hours_per_day INT,
    dias_disponibles VARCHAR(50) -- Lista de días en un formato (ejemplo: '1, 3, 5')
);

CREATE TABLE skill (
    id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE employee_skill (
    employee_id INT,
    skill_id INT,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id),
    PRIMARY KEY (employee_id, skill_id)
);

CREATE TABLE task (
    id INT PRIMARY KEY,
    title VARCHAR(100),
    due_date DATE,
    time_use INT
);

CREATE TABLE task_skill_set (
    task_id INT,
    skill_id INT,
    FOREIGN KEY (task_id) REFERENCES task(id),
    FOREIGN KEY (skill_id) REFERENCES skill(id),
    PRIMARY KEY (task_id, skill_id)
);

CREATE TABLE assignment (
    id INT PRIMARY KEY,
    employee_id INT,
    task_id INT,
    date_assignment DATE,
    hour_assignment INT,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (task_id) REFERENCES task(id)
);
