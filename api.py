from flask import Blueprint, request, jsonify
from models import db, Payment, BioData, Student


student_bp = Blueprint('student_bp',__name__, url_prefix='/student')


@student_bp.route('/all')
def payments():
    payments= Payment.query.all()
    payments_json= [payment.to_dict() for payment in payments]
    return jsonify(payments_json)


@student_bp.route('/new', methods=['POST', 'GET'])
def new_payment():

    if request.method== 'POST':
        data = request.json

        new_payment = Payment(description=data.get('description'), amount= data.get('amount'), student_id=data.get('student_id'))
        db.session.add(new_payment)
        db.session.commit()
        return {'msg':'payment successfull'}
    

@student_bp.route('/biodata/<int:id>')
def get_bio_data(id):
    bio_data= BioData.query.filter_by(id=id).first()
    
    return jsonify(bio_data.to_dict())



@student_bp.route('/newbiodata/<int:id>', methods=['POST', 'GET'])
def new_bio_data(id):
    student = Student.query.filter_by(id=id).first()
    if request.method== 'POST':
        data = request.json
        new_bio = BioData(hometown=data.get('hometown'), location= data.get('location'))
        student.bio_data = new_bio
        db.session.add(new_bio)
        db.session.commit()
        return {'msg':'Bio Created successfully'}
    


