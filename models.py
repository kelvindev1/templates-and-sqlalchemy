from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()

class Student(db.Model,SerializerMixin):
    serialize_rules=('-payments.student',)
    __tablename__='students'
    id= db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    payments = db.relationship('Payment',back_populates='student')
    bio_data = db.relationship('BioData',back_populates='student', uselist=False)



class Payment(db.Model,SerializerMixin):
    serialize_rules=('-student.payments',)
    id= db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(400))
    amount = db.Column(db.Float(), nullable=False)
    student_id= db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student',back_populates='payments')


class BioData(db.Model,SerializerMixin):
    serialize_rules=('-student.bio_data','-student.payments')
    id= db.Column(db.Integer, primary_key=True)
    hometown= db.Column(db.String)
    location=  db.Column(db.String)
    student_id= db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student',back_populates='bio_data')
