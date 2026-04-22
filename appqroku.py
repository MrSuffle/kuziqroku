from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Şifre listelerin
gecerli_sifreler = ["940708b7", "Giris2026", "OzelKod99", "Admin44"]
kullanilmis_kodlar = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kontrol', methods=['POST'])
def kontrol():
    data = request.json
    qr_verisi = data.get('qr_verisi')

    # Mantık Kontrolü
    if qr_verisi in gecerli_sifreler:
        if qr_verisi not in kullanilmis_kodlar:
            kullanilmis_kodlar.add(qr_verisi)
            return jsonify({"status": "GECBILIR", "message": f"Giris Onaylandi: {qr_verisi}", "color": "green"})
        else:
            return jsonify({"status": "GECEMEZ", "message": "Bu kod daha once kullanildi!", "color": "orange"})
    else:
        return jsonify({"status": "GECEMEZ", "message": "Gecersiz Sifre!", "color": "red"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)