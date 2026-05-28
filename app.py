from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Resimlerin kaydedileceği yer (static/yuklenenler klasörü)
# İleride bir USB bellek veya SD kart takarsan buraya "E:/yuklenenler" gibi o sürücünün yolunu yazabilirsin!
UPLOAD_FOLDER = os.path.join('static', 'yuklenenler')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Proje İş Planındaki "Haftalık Sabit Ortalama" simulasyonu
HAFTALIK_ORTALAMA = 1000 

# Geçici veri tabanımız (Örnek resimleri internetten çekip simüle ediyoruz)
resimler_veritabani = [
    {"url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5", "izlenme": 4500, "komisyon": 10},
    {"url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab", "izlenme": 1200, "komisyon": 10},
    {"url": "https://images.unsplash.com/photo-1561214115-f2f134cc4912", "izlenme": 800, "komisyon": 10}
]

# Dinamik Komisyon Hesaplama Fonksiyonu (Dökümandaki Algoritman)
def komisyon_hesapla(izlenme):
    if izlenme >= HAFTALIK_ORTALAMA * 4:
        return 20  # Ortalamanın 4 katı ise %20
    elif izlenme >= HAFTALIK_ORTALAMA * 3:
        return 15  # Ortalamanın 3 katı ise %15
    return 10      # Başlangıç seviyesi %10

@app.route('/')
def ana_sayfa():
    # Her resmin komisyonunu izlenmesine göre haftalık baraja göre güncelle
    for resim in resimler_veritabani:
        resim['komisyon'] = komisyon_hesapla(resim['izlenme'])
    return render_template('index.html', resimler=resimler_veritabani, baraj=HAFTALIK_ORTALAMA)

@app.route('/yukle', methods=['POST'])
def resim_yukle():
    if 'dosya' not in request.files:
        return redirect(url_for('ana_sayfa'))
    
    dosya = request.files['dosya']
    if dosya.filename != '':
        # Klasör yoksa otomatik oluşturur
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
            
        dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], dosya.filename)
        dosya.save(dosya_yolu)
        
        # Yeni yüklenen resmi sıfır izlenme ile listeye ekle
        yeni_resim = {
            "url": "/" + dosya_yolu.replace('\\', '/'),
            "izlenme": 0,
            "komisyon": 10
        }
        resimler_veritabani.append(yeni_resim)
        
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)