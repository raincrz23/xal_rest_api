# xal_rest_api
Rest API para el challenge

Intenté instalar Docker en mi computadora portátil, sin embargo, parece que faltaban ciertas configuraciones o archivos para que funcione correctamente. Creo que tuvo que ver con una cierta actualización de wsl, sin embargo, dado que esta es mi computadora portátil de trabajo que estoy usando, no pude instalar el archivo de actualización debido a las restricciones que mi empresa impuso en nuestras máquinas. Sin embargo, dado esto, intenté mantener la API lo más simple posible usando solo python y postgres 13.

Versiones de:
    Python == 3.7
    Flask == 2.0.1
    Flask-SQLAlchemy == 2.5.1
    marshmallow == 3.12.1
    pip == 21.2.4
    psycopg2-binary == 2.8.6
    SQLAlchemy == 1.4.17

Si python está instalado con pip, adquirir los paquetes necesarios para que la aplicación funcione es muy sencillo con el archivo proporcionado 'requirements.txt'

    pip install -r requirements.txt

El siguiente paso también es muy sencillo. Una vez que se crea una base de datos en postgres, conectarla a la aplicación es solo cuestión de reemplazar la siguiente línea en el código con los parámetros correctos:

Se modifica esta ruta para conectar a la base de datos 
El formato es el siguiente : 'postgresql://usuario:contraseña@ruta-al-servidor/nombre-del-database'

Linea-8 en app.py
    app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:postgres@localhost/xal' # ejemplo

Una vez configurada correctamente la ruta, el siguiente paso sería crear las tablas para la aplicación. En este escenario, elegí crear dos tablas (Employee, Department) con una relación de many-to-many.

La razón de esto es que luego de analizar el csv proporcionado, se ve que una persona (empleado en este caso) puede pertenecer a más de un departamento y por lo tanto, un departamento puede tener más de un empleado. Por supuesto, esto podría haber sido modelado con otras tablas como con una de las empresas, sin embargo, para simplificar, elegí solo estas dos.

Ejecutar el archivo create_tables.py creará automáticamente las tablas en la base de datos, dado que la ruta está configurada correctamente. Se crearán tres tablas: (employee, department, employee_department)

Ejecute el siguiente comando:

    python create_tables.py

Además, proporcioné consultas sql para insertar registros en las tablas para probar las peticiones GET. Solo he proporcionado 3 registros, el motivo es que al realizar la llamada POST para agregar un nuevo empleado, se arroja un error debido a un bug en el paquete psycopg2.

    (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "employee_pkey"
        DETAIL:  Key (employee_id)=(1) already exists.

Por molesto que sea, el problema se resuelve repitiendo la llamada tres veces más para que el employee_id se establezca en 4, lo que corresponde a un nuevo registro en la tabla.

Las peticiones GET, POST, PUT, DELETE actuarán sobre los objetos del empleado y requerirán datos en formato json para los métodos POST y PUT:

    GET /all_employees
    Devuelve todos los registros de la tabla de empleados.

    GET /employee/<int:id>
    Devuelve el empleado correspondiente del id proporcionado.

    POST /add_employee
    Crea un nuevo registro en la tabla de empleados. Es importante señalar que los departamentos a los que corresponde el empleado es solo una lista en el mismo json.

    ejemplo:
    {
        "first_name": "Veronika",
        "last_name": "Inouye",
        "company_name": "C 4 Network Inc",
        "address": "6 Greenleaf Ave",
        "city": "San Jose",
        "state": "CA",
        "zip": 95111,
        "phone1": "408-540-1785",
        "phone2": "408-813-4592",
        "email": "vinouye@aol.com",
        "departments": [
            "Sales",
            "Finances"
        ]
    }

    PUT /employee/<int:id>
    Actualiza el empleado correspondiente dado el id proporcionado. Este método actualizará uno o más parámetros del empleado, excepto los departamentos.

    ejemplo:
    {
        "phone2": "555-555-5555",
        "email": "new_email@aol.com",
    }

    DELETE /employee/<int:id>
    Elimina el registro correspondiente, junto con sus relaciones empleado-departamento, dado el id proporcionado.