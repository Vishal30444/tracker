from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # normal, manager, supervisor
    approved = db.Column(db.Boolean, default=False)  # Signup approval flag

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Project model with approval fields
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thematic_area = db.Column(db.String(120), nullable=False)
    project_title = db.Column(db.Text, nullable=False)
    continent = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    city_state = db.Column(db.Text, nullable=False)  #added
    funding_agency = db.Column(db.Text, nullable=False)
    final_funder = db.Column(db.Text, nullable=False)   #added
    type_of_procurement = db.Column(db.Text, nullable=False)
    
    budget = db.Column(db.Text, nullable=False)
    currency_type = db.Column(db.Text, nullable=False)
    opportunity_published_date = db.Column(db.Text, nullable=False)  #added
    deadline = db.Column(db.Text, nullable=False)
    project_duration = db.Column(db.Text, nullable=False)
    key_expert= db.Column(db.Text, nullable=False)
    non_key_expert=db.Column(db.Text, nullable=False)
    proposed_contract_type = db.Column(db.Text, nullable=False)  #added
    objectives = db.Column(db.Text, nullable=False)
    links = db.Column(db.Text, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    
    created_on = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')).replace(second=0, microsecond=0))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Manager fields
    manager_status = db.Column(db.String(20), default='Pending')  # Approved/Rejected/Pending
    manager_comments = db.Column(db.Text)
    
    # Supervisor fields
    supervisor_status = db.Column(db.String(20), default='Pending')  # Approved/Rejected/Pending
    supervisor_comments = db.Column(db.Text)
