from datetime import date, datetime
from dataclasses import dataclass
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Modell for SQLAlchemy Classes
# @dataclass for JSON-Serialization
@dataclass
class Budget(db.Model):
    created: date
    description: str
    spending: int
    income: int
    date: date

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(128))
    spending = db.Column(db.Integer)
    income = db.Column(db.Integer)
    date = db.Column(db.Date)


    def __repr__(self):
        return '<Budget {}>'.format(self.description)

@dataclass
class User(UserMixin, db.Model):
    budget: Budget
    created: date
    firstname: str
    lastname: str
    username: str
    spending_limit: int
    email: str
    adminuser: bool
    

    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, index=True, primary_key=True)
    api_key = db.Column(db.String(80))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    u_pw = db.Column(db.String(128))
    spending_limit = db.Column(db.Integer, default=1000)
    email  = db.Column(db.String(128), index=True, unique=True)
    adminuser = db.Column(db.Boolean, default=False)
    budget = db.relationship(Budget)

    def set_password(self, password):
        self.u_pw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.u_pw, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@login.user_loader
def load_user(id):
    return User.query.get(int(id))