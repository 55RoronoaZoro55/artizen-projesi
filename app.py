import os
import random
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cok_gizli_bir_anahtar')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'admin@artizens.dev')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'hkyepunkgqvviwtz')

db = SQLAlchemy(app)
mail = Mail(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session: return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)

with app.app_context(): db.create_all()

# --- ROTALAR ---

@app.route('/')
def index():
    return render_template('index.html') # Ana sayfanı index.html olarak okur

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')
        privacy = request.form.get('privacy')

        if not terms or not privacy: return "Error: You must accept terms!"
        if password != confirm_password: return "Error: Passwords do not match!"
        if len(password) < 8: return "Error: Min 8 characters!"
        
        if User.query.filter_by(username=username).first(): return "Error: Username taken!"
        if User.query.filter_by(email=email).first(): return "Error: Email taken!"

        code = str(random.randint(100000, 999999))
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, email=email, password=hashed_password, 
                        verification_code=code, is_active=False)
        
        db.session.add(new_user)
        db.session.commit()

        try:
            msg = Message("Verify Your Account", sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"Your code is: {code}"
            mail.send(msg)
            return "Registration successful! Please check your email."
        except Exception as e:
            return f"Error: {str(e)}"
            
    return render_template('signup.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_code = request.form.get('code')
        user = User.query.filter_by(verification_code=user_code).first()
        if user:
            user.is_active = True
            user.verification_code = None
            db.session.commit()
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index')) # Doğrulama sonrası ana sayfaya gönderir
        return "Invalid code!"
    return '<form method="POST"><input name="code" placeholder="Enter code"><button>Verify</button></form>'

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {session['username']}! <a href='/logout'>Çıkış Yap</a>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index')) # Çıkış yapınca ana sayfaya döner

if __name__ == '__main__':
    app.run()