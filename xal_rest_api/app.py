from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app=Flask(__name__)
# Modifica esta ruta para conectar a la base de datos 
# El formato es el siguiente : 'postgresql://usuario:contraseña@ruta-al-servidor/nombre-del-database'
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:postgres@localhost/xal' # ejemplo
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

employee_department = db.Table('employee_department',
    db.Column('department_id', db.Integer, db.ForeignKey('department.department_id'), primary_key=True),
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True)
)

class Department(db.Model):
    __tablename__ = 'department'

    department_id = db.Column(db.Integer(),primary_key=True)
    department_name = db.Column(db.String(255),nullable=False)


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer(),primary_key=True)
    first_name = db.Column(db.String(255),nullable=False)
    last_name = db.Column(db.String(255),nullable=False)
    company_name = db.Column(db.String(255),nullable=False)
    address = db.Column(db.String(255),nullable=True)
    city = db.Column(db.String(255),nullable=True)
    state = db.Column(db.String(255),nullable=True)
    zip = db.Column(db.Integer(),nullable=True)
    phone1 = db.Column(db.String(255),nullable=False)
    phone2 = db.Column(db.String(255),nullable=True)
    email = db.Column(db.String(255),nullable=False)
    departments = db.relationship('Department', secondary=employee_department, lazy='subquery',
        backref=db.backref('employees', lazy=True))

    def __repr__(self):
        return self.last_name + ' , ' + self.first_name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class DepartmentSchema(Schema):

    department_id = fields.Integer()
    department_name = fields.String()

class EmployeeSchema(Schema):

    employee_id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()
    address = fields.String()
    city = fields.String()
    state = fields.String()
    zip = fields.Integer()
    phone1 = fields.String()
    phone2 = fields.String()
    email = fields.String()
    departments = fields.List(fields.Nested(DepartmentSchema))

@app.route('/all_employees',methods=['GET'])
def get_all_employees():
    employees = Employee.get_all()
    serializer = EmployeeSchema(many=True)

    data = serializer.dump(employees)

    return jsonify(data)


@app.route('/add_employee',methods=['POST'])
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name = data.get('first_name'),
        last_name = data.get('last_name'),
        company_name = data.get('company_name'),
        address = data.get('address'),
        city = data.get('city'),
        state = data.get('state'),
        zip = data.get('zip'),
        phone1 = data.get('phone1'),
        phone2 = data.get('phone2'),
        email = data.get('email'),
        #departments = data.get('department')
    )
    deps = data.get('departments')
    for d in deps:
        dpp = db.session.query(Department).filter_by(department_name=d).first()
        new_employee.departments.append(dpp)
    print(new_employee)

    new_employee.save()

    serializer = EmployeeSchema()

    data = serializer.dump(new_employee)

    return jsonify(data),201

@app.route('/employee/<int:id>',methods=['GET'])
def get_employee(id):
    employee = Employee.get_by_id(id)

    serializer = EmployeeSchema()

    data = serializer.dump(employee)

    return jsonify(data),200

@app.route('/employee/<int:id>',methods=['PUT'])
def update_employee(id):
    employee_to_update = Employee.get_by_id(id)

    data = request.get_json()

    # Usamos if en vez de else if porq en el caso de que hay multiples parametros del objeto para actualizar,
    # El else if va cumplir con el primer caso que encuentra como True y saltara todos los demas 
    if data.get('first_name'):
        employee_to_update.first_name = data.get('first_name')

    if data.get('last_name'):
        employee_to_update.last_name = data.get('last_name')

    if data.get('company_name'):
        employee_to_update.company_name = data.get('company_name')
    
    if data.get('address'):
        employee_to_update.address = data.get('address')

    if data.get('city'):
        employee_to_update.city = data.get('city')
    
    if data.get('state'):
        employee_to_update.state = data.get('state')
    
    if data.get('zip'):
        employee_to_update.zip = data.get('zip')

    if data.get('phone1'):
        employee_to_update.phone1 = data.get('phone1')
    
    if data.get('phone2'):
        employee_to_update.phone2 = data.get('phone2')
    
    if data.get('email'):
        employee_to_update.email = data.get('email')
    
    #if data.get('departments'):
    #    employee_to_update.departments = data.get('departments')

    db.session.commit()

    serializer = EmployeeSchema()

    employee_data = serializer.dump(employee_to_update)

    return jsonify(employee_data),200

@app.route('/employee/<int:id>',methods=['DELETE'])
def delete_employee(id):
    employee_to_delete = Employee.get_by_id(id)

    employee_to_delete.delete()

    return jsonify({"message":"Deleted"}),204

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}),500

if __name__ == '__main__':
    app.run(debug=True)