from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Örnek: Şifre kaydederken
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    # Şifreyi veritabanına asla açık yazma, hash'le!
    hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
    
    # Burada veritabanı işlemine (PostgreSQL/SQLite) devam et...
    return "Kullanıcı güvenli bir şekilde kaydedildi."

# Örnek: Giriş yaparken
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Veritabanından gelen hash'i kontrol et
    # stored_password = db.get_user_password(username)
    # if check_password_hash(stored_password, password):
    #     return "Giriş başarılı"
    return "Hatalı giriş"