from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' # Güvenlik için bunu mutlaka değiştir

# Veritabanı Ayarları
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail (SMTP) Ayarları - Google Workspace
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'admin@artizens.dev'
app.config['MAIL_PASSWORD'] = 'hkyepunkgqvviwtz'

db = SQLAlchemy(app)
mail = Mail(app)

# Kullanıcı Modeli
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')

        if not terms:
            return "Error: You must accept the terms of service!"
        if password != confirm_password:
            return "Error: Passwords do not match!"

        code = str(random.randint(100000, 999999))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password=hashed_password, 
                        verification_code=code, is_active=False)
        
        db.session.add(new_user)
        db.session.commit()

        # Resmi Doğrulama Maili
        msg = Message("Welcome to Artizen - Verify Your Account", 
                      sender=('Artizen Team', 'admin@artizens.dev'), 
                      recipients=[email])
        
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Welcome to Artizen!</h2>
            <p>Thank you for joining our platform. To complete your registration and activate your account, please use the following verification code:</p>
            <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                {code}
            </div>
            <p>If you did not initiate this registration, please ignore this email.</p>
            <br>
            <p>Best regards,<br><strong>The Artizen Team</strong></p>
        </div>
        """
        try:
            mail.send(msg)
            return "Registration successful! Please check your email for the verification code and go to /verify."
        except Exception as e:
            return f"Error sending email: {str(e)}"
        
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
            return "Your account has been successfully verified!"
        return "Invalid code!"
    return '<form method="POST"><input name="code" placeholder="Enter code"><button>Verify</button></form>'

if __name__ == '__main__':
    app.run(debug=True)