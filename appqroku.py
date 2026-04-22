from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "cok_gizli_anahtar" # Session güvenliği için gerekli

# AYARLAR
ANA_GIRIS_SIFRESI = "12345"  # Siteye girerken sorulacak şifre
gecerli_sifreler = ["940708b7", "Giris2026", "OzelKod99", "Admin44"]
kullanilmis_kodlar = set()

@app.route('/')
def index():
    # Eğer kullanıcı giriş yapmadıysa login sayfasına yönlendir
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    sifre = data.get('sifre')
    
    if sifre == ANA_GIRIS_SIFRESI:
        session['logged_in'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Yanlış Şifre!"})

@app.route('/kontrol', methods=['POST'])
def kontrol():
    if not session.get('logged_in'):
        return jsonify({"status": "HATA", "message": "Yetkisiz Erişim!"})

    data = request.json
    qr_verisi = data.get('qr_verisi')

    if qr_verisi in gecerli_sifreler:
        if qr_verisi not in kullanilmis_kodlar:
            kullanilmis_kodlar.add(qr_verisi)
            return jsonify({"status": "GECBILIR", "message": f"Onaylandı: {qr_verisi}", "color": "green"})
        else:
            return jsonify({"status": "GECEMEZ", "message": "Bu kod zaten kullanıldı!", "color": "orange"})
    else:
        return jsonify({"status": "GECEMEZ", "message": "Geçersiz Şifre!", "color": "red"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)