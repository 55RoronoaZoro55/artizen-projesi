from flask import Flask, render_template

app = Flask(__name__)

# Ana sayfa (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Giriş sayfası (login.html)
@app.route('/login')
def login():
    return render_template('login.html')

# Kayıt sayfası (signup.html)
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Gizlilik sayfası (privacy.html)
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Kullanım koşulları sayfası (terms.html)
@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == "__main__":
    app.run(debug=True)