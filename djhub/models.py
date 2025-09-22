from djhub.extensions import db
from datetime import datetime

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    genres = db.Column(db.String(200))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120))
    date = db.Column(db.Date)
    budget = db.Column(db.Integer)
    genres = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return f"<Profile {self.username}>"
