from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Şifre hash'leneceği için uzunluğu 200 yaptık
    is_active = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)