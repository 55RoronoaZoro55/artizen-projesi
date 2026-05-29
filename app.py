from flask import Flask, render_template, request
from models import db # models.py dosyasından db'yi çağırıyoruz

app = Flask(__name__)

# Veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını uygulamaya bağla
db.init_app(app)

# Tabloları oluştur (Uygulama ilk başladığında çalışır)
with app.app_context():
    db.create_all()

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Kayıt sayfası (Sign Up)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Formdan gelen verileri al
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # ... burada kullanıcıyı veritabanına ekleme kodları gelecek
        return "Sign Up form received and ready to save!"
    return render_template('signup.html')

# Giriş sayfası (Log In)
@app.route('/login')
def login():
    return render_template('login.html')

# Hukuki Sayfalar
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    app.run(debug=True)