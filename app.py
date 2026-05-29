from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash # Şifreleri güvenli hale getirmek için

app = Flask(__name__)
app.secret_key = 'gizli-anahtar-buraya' # Flash mesajları için gerekli

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

        # 1. Hukuki Onay Kontrolü
        if not terms:
            return "Hata: Kayıt olabilmek için Hizmet Şartlarını kabul etmelisiniz!"

        # 2. Şifre Eşleşme Kontrolü
        if password != confirm_password:
            return "Hata: Şifreler birbiriyle eşleşmiyor!"

        # 3. Veritabanı (Zaten kayıtlı mı?) Kontrolü
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            return "Bu kullanıcı adı veya e-posta zaten kullanımda!"

        # 4. Kayıt İşlemi (Şifreyi hash'leyerek kaydet)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return "Kayıt başarıyla oluşturuldu! E-posta doğrulama adımına geçebilirsiniz."

    return render_template('signup.html')

# Diğer rotaların aynı kalabilir...
if __name__ == '__main__':
    app.run(debug=True)