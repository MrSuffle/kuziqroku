from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "cok_gizli_anahtar"

# ŞİFRELER
ANA_GIRIS_SIFRESI = "12345"    # Siteye ilk girişte sorulan
DUZENLEME_SIFRESI = "admin99"  # Listeye geri dönmek için sorulan

# Global Değişkenler
gecerli_sifreler = []
kullanilmis_kodlar = set()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data and data.get('sifre') == ANA_GIRIS_SIFRESI:
        session['logged_in'] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Hatalı Giriş!"})

@app.route('/sifreleri_kaydet', methods=['POST'])
def sifreleri_kaydet():
    global gecerli_sifreler, kullanilmis_kodlar
    data = request.json
    raw_text = data.get('liste', '')
    
    yeni_liste = [line.strip() for line in raw_text.split('\n') if line.strip()]
    if not yeni_liste:
        return jsonify({"success": False, "message": "Lütfen şifre girin!"})

    gecerli_sifreler = yeni_liste
    kullanilmis_kodlar = set()
    return jsonify({"success": True, "count": len(gecerli_sifreler)})

@app.route('/duzenleme_kontrol', methods=['POST'])
def duzenleme_kontrol():
    # Düzenleme butonu için şifre kontrolü
    data = request.json
    if data.get('sifre') == DUZENLEME_SIFRESI:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Düzenleme şifresi hatalı!"})

@app.route('/kontrol', methods=['POST'])
def kontrol():
    if not session.get('logged_in'):
        return jsonify({"status": "HATA", "message": "Oturum kapalı!"})

    data = request.json
    qr_verisi = str(data.get('qr_verisi')).strip()

    if qr_verisi in gecerli_sifreler:
        if qr_verisi not in kullanilmis_kodlar:
            kullanilmis_kodlar.add(qr_verisi)
            return jsonify({"status": "GECBILIR", "message": f"ONAY: {qr_verisi}", "color": "green"})
        else:
            return jsonify({"status": "GECEMEZ", "message": "Daha önce okutuldu!", "color": "orange"})
    else:
        return jsonify({"status": "GECEMEZ", "message": "Listede yok!", "color": "red"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)