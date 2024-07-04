from flask import  Flask, render_template, url_for, request, redirect
from flask_migrate import Migrate
from api import student_bp 
from auth import jwt,auth_bp, bcrypt, allow
from datetime import timedelta

from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///school.db'
app.config['SECRET_KEY'] ='ab1479e159f8b60fc6ade3e987a306'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=4)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)

app.register_blueprint(student_bp)
app.register_blueprint(auth_bp)
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app=app, db=db)




@app.route('/student/<int:id>/')
def single_student(id):
    student = Student.query.filter_by(id=id).first()
    print(student.payments)
    print(student.bio_data)
    return render_template('index.html', student= student)


@app.route('/update_student/<int:id>/', methods=['POST','GET'])
def update_student(id):
    student = Student.query.filter_by(id=id).first()
    if request.method=='POST':
        data = request.form
        student.first_name = data.get('first_name')
        student.last_name = data.get('last_name')
        student.email = data.get('email')
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('all_students'))
        
    
    return render_template('update-student.html', student= student)

@app.route('/delete_student/<int:id>/', methods=['POST','GET'])
def delete_student(id):
    student = Student.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('all_students'))

@app.route('/')
def home():
    return {"msg":"home"}


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/students')
def all_students():
    students = Student.query.all()
    print(students)

    return render_template('students.html',students=students )

@app.route('/add_student', methods=['POST','GET'])
def create_student():

    if request.method=='POST':
        data = request.form
        new_student = Student(first_name =data.get('first_name'),last_name =data.get('last_name'),email =data.get('email'))
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('all_students'))

    return render_template('add-student.html')





