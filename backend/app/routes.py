import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import db, User, Resume, Job, Application
from utils import get_application_status_badge
from job_matcher import get_job_recommendation
from cv_parser import parse_cv

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

bcrypt = Bcrypt(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username, "email": user.email}}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        resume = Resume.query.filter_by(user_id=current_user.id).first()
        return jsonify({"username": current_user.username, "email": current_user.email, "resume": resume.to_dict() if resume else None})
    
    data = request.get_json()
    current_user.username = data['username']
    current_user.email = data['email']
    
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        resume = Resume(user_id=current_user.id, skills=data['skills'], experience=data['experience'], education=data['education'])
        db.session.add(resume)
    else:
        resume.skills = data['skills']
        resume.experience = data['experience']
        resume.education = data['education']
    
    db.session.commit()
    return jsonify({"message": "Profile updated"}), 200

@app.route('/upload_cv', methods=['POST'])
@login_required
def upload_cv():
    file = request.files['cv_file']
    file_content = file.read().decode('utf-8', errors='ignore')
    parsed_data = parse_cv(file_content)
    
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if resume:
        resume.skills = parsed_data['skills']
        resume.experience = parsed_data['experience']
        resume.education = parsed_data['education']
    else:
        resume = Resume(user_id=current_user.id, skills=parsed_data['skills'], experience=parsed_data['experience'], education=parsed_data['education'])
        db.session.add(resume)
    
    db.session.commit()
    return jsonify({"message": "CV uploaded successfully"}), 200

@app.route('/jobs', methods=['GET'])
@login_required
def get_jobs():
    job_recommendation = get_job_recommendation(current_user.id)
    return jsonify(job_recommendation), 200

@app.route('/apply_job/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    existing_application = Application.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if existing_application:
        return jsonify({"message": "Already applied"}), 400
    
    application = Application(user_id=current_user.id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Application submitted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
