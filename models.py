from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



student_course = db.Table(
    "student_course",
    metadata,
    db.Column("student_id",db.ForeignKey("students.id")),
    db.Column("course_id", db.ForeignKey("course.id")),
)

user_roles = db.Table(
    "user_roles",
    metadata,
    db.Column("role_id",db.ForeignKey("role.id")),
    db.Column("user_id", db.ForeignKey("users.id")),
)
class User(db.Model):
    __tablename__='users'
    id= db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    roles = db.relationship('Role',back_populates='user', secondary=user_roles)

class Role(db.Model):
    __tablename__='role'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(255))
    user = db.relationship('User',back_populates='roles', secondary=user_roles)


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

class Student(db.Model,SerializerMixin):
    serialize_rules=('-payments.student',)
    __tablename__='students'
    id= db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    payments = db.relationship('Payment',back_populates='student')
    bio_data = db.relationship('BioData',back_populates='student', uselist=False)
    courses = db.relationship('Course', back_populates='student', secondary=student_course)

class Course(db.Model):
    __tablename__ ='course'
    id= db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String)
    passmark =  db.Column(db.Float)
    student = db.relationship('Student', back_populates='courses', secondary=student_course)

class Payment(db.Model,SerializerMixin):
    __tablename__ ='payment'
    serialize_rules=('-student.payments',)
    id= db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    amount = db.Column(db.Float(), nullable=False)
    student_id= db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student',back_populates='payments')


class BioData(db.Model,SerializerMixin):
    __tablename__ ='biodata'
    serialize_rules=('-student.bio_data','-student.payments')
    id= db.Column(db.Integer, primary_key=True)
    hometown= db.Column(db.String)
    location=  db.Column(db.String)
    student_id= db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student',back_populates='bio_data')



