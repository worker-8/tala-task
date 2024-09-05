# tala-task
Proyecto de prueba tecnica para Talana. Se decidio hacer con Python utilizado el framework flask y como base de datos SQLite, esta desicion se tomo en virtud al tiempo asi mismo minimizar la posibilidad de fallo por configuraciones.

## Requerimientos Docker.

- Make 3.81
- Docker version 24.0.2

### Pasos a seguir.

1. ejecutar el siguiente comando para construir el contenedor.
```bash
make build
```
2. ejecutar el siguiente comando para que el contenedor se inicie.
```bash
make run
```

## Requerimientos correr directo.

- Python 3.12.5 
- Make 3.81

### Pasos a seguir.

1. validar las versiones minimas requeridas
2. ejecutar el siguiente comando para generar el enviroment
```bash
make env
```
3. ejecutar el siguiente comando para generar la base de datos (sqlite)
```bash
make db-regen
```

4. ejecutar el siguiente comando para iniciar el servidor
```bash
make server
```

## Modelo de datos
![image](https://github.com/worker-8/tala-task/blob/main/docu/image.png?raw=true)
para lograr el objetivo de la prueba se genero el siguiente modelo de datos
*PD: en la tabla task se añade el campo is_assignment*

## Endpoints.

### find_employee
lista a los employees.

```bash
curl --request GET \
  --url http://localhost:5000/api/v1/employee
```

### find_task
lista las task

```bash
curl --request GET \
  --url http://localhost:5000/api/v1/task 
```

### find_skill
lista las skills
```bash
curl --request GET \
  --url http://localhost:5000/api/v1/skill 
```

### assignment
gatillas el proceso de asignacion de tareas.
```bash
curl --request GET \
  --url http://localhost:5000/api/v1/task/assignment \
  --header 'User-Agent: insomnia/9.3.3'
```

### create_employee
crea un employee

```bash
curl --request POST \
  --url http://localhost:5000/api/v1/employee \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.3' \
  --data '{
	"employee_name": "Jaime",
	"hours_per_day": 8,
	"available_days": "1,2,3,4,5",
	"skill_set": "1,2,5"
}'
```

|name|value|descripcion|
|----|-----|-----------|
|employee_name|Jaime|(string)nombre del empleado|
|hours_per_day|8|(number 1-8)cantidad horas trabajadas|
|available_days|1,2,3,4,5|(string)corresponde a los numeros de dia de la semana lunes:1 .. viernes:5|
|skill_set|1,2,5|(string) ids de skills que posee el employee revisar en el [endpoint](#find_skill)|

### create_task
crea una task

```bash
curl --request POST \
  --url http://localhost:5000/api/v1/task \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.3' \
  --data '{
	"title": "test 3: something",
	"due_date": "2024-09-10",
	"time_use": "4",
	"skill_set": "2"
}'
```
|name|value|descripcion|
|----|-----|-----------|
|title|Tarea 1|(string)nombre de la tarea|
|due_date|2024-09-01|(date) fecha de termino de la tarea formato **YYYY-MM-DD** |
|time_use|4|(number 1-8)cantidad horas destinadas a la tarea|
|skill_set|1,2,5|(string) ids de skills que posee el employee revisar en el [endpoint](#find_skill)|
### create_skill
crea una skill

```bash
curl --request POST \
  --url http://localhost:5000/api/v1/skill \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/9.3.3' \
  --data '{
	"skill_name": "UX/UI"
}'
```
|name|value|descripcion|
|----|-----|-----------|
|skill_name|UX/UI|(string)nombre de la habilidad|

### Upload CSV
se pueden llenar de forma grupal a travez de los cargadores de CSV a coninuacion dejare las paths

**Employees**: 
- archivo [ref](https://raw.githubusercontent.com/worker-8/tala-task/main/docu/employees.csv)
- url: http://localhost:5000/api/v1/employee/csv

**Skills**: 
- archivo [ref](https://raw.githubusercontent.com/worker-8/tala-task/main/docu/skills.csv)
- url: http://localhost:5000/api/v1/skill/csv

**Tasks**: 
- archivo [ref](https://raw.githubusercontent.com/worker-8/tala-task/main/docu/tasks.csv)
- url: http://localhost:5000/api/v1/task/csv

## Cosas que faltaron

- pruebas unitarias.
- Validar que Skills y Employees no se repetieran.
- En caso de actividades mas largas que las horas disponibles, fraccionarlas.
- Endpoint de reporte.
- Mejorar mecanismo de reparto de tareas.
- Agregar una prioridad a cada tarea para posicionarlas mejor en la lista.
