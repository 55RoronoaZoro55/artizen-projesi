from flask import Flask, render_template, request

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Kayıt sayfası
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Burada kullanıcı bilgilerini alıp işleyeceğiz (ileride buraya mail doğrulama gelecek)
        username = request.form.get('username')
        email = request.form.get('email')
        # ... kayıt mantığı burada olacak
        return "Sign Up form received!"
    return render_template('signup.html')

# Giriş sayfası
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