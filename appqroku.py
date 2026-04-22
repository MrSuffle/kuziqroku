from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "cok_gizli_anahtar"

# AYARLAR
ANA_GIRIS_SIFRESI = "12345"
# Şifreleri bellekte tutacağız
gecerli_sifreler = []
kullanilmis_kodlar = set()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    # Giriş yapılmışsa dosya yükleme/kontrol panelini göster
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('sifre') == ANA_GIRIS_SIFRESI:
        session['logged_in'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Yanlış Şifre!"})

@app.route('/upload_txt', methods=['POST'])
def upload_txt():
    global gecerli_sifreler, kullanilmis_kodlar
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Dosya seçilmedi!"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "Dosya adı boş!"})

    if file and file.filename.endswith('.txt'):
        # Dosyayı oku ve şifreleri listeye al
        content = file.read().decode('utf-8')
        gecerli_sifreler = [line.strip() for line in content.splitlines() if line.strip()]
        kullanilmis_kodlar = set() # Yeni dosya yüklenince eski kullanılanları sıfırla
        
        return jsonify({
            "success": True, 
            "count": len(gecerli_sifreler),
            "message": f"{len(gecerli_sifreler)} adet şifre başarıyla yüklendi."
        })
    
    return jsonify({"success": False, "message": "Sadece .txt dosyası yükleyebilirsiniz!"})

@app.route('/kontrol', methods=['POST'])
def kontrol():
    if not session.get('logged_in'):
        return jsonify({"status": "HATA", "message": "Yetkisiz!"})

    data = request.json
    qr_verisi = data.get('qr_verisi')

    if qr_verisi in gecerli_sifreler:
        if qr_verisi not in kullanilmis_kodlar:
            kullanilmis_kodlar.add(qr_verisi)
            return jsonify({"status": "GECBILIR", "message": f"ONAYLANDI: {qr_verisi}", "color": "green"})
        else:
            return jsonify({"status": "GECEMEZ", "message": "Bu kod zaten kullanıldı!", "color": "orange"})
    else:
        return jsonify({"status": "GECEMEZ", "message": "Listede Yok!", "color": "red"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)