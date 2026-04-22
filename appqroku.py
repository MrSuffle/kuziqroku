import cv2

# Ayarlar
gecerli_sifreler = ["940708b7", "Giris2026", "OzelKod99", "Admin44"]
kullanilmis_kodlar = set()

# Kontrol değişkeni (Senin istediğin 'a' mantığı)
a_degeri = 0 

detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

print("--- SISTEM BASLATILDI ---")
print("1. Tarama yapmak için 'a' tuşuna basın.")
print("2. Sistemi tekrar aktif etmek (sıfırlamak) için 'c' tuşuna basın.")
print("3. Çıkış için 'q' tuşuna basın.")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Klavye girişlerini kontrol et
    key = cv2.waitKey(1) & 0xFF

    # 'a' tuşuna basılırsa tarama moduna gir
    if key == ord('a'):
        if a_degeri == 0:
            print("\n[BILGI] Tarama yapılıyor... QR kodu gösterin.")
            # a_degeri'ni hemen artırmıyoruz, başarılı okuma yapınca artıracağız
        else:
            print(f"\n[UYARI] Sistem kilitli (a={a_degeri}). Lütfen önce 'c' ile sıfırlayın.")

    # 'c' tuşuna basılırsa sistemi sıfırla
    if key == ord('c'):
        a_degeri = 0
        print("\n[SISTEM] SIFIRLANDI. Yeni tarama için 'a' tuşuna basabilirsiniz.")

    # EĞER a_degeri 0 ise QR TARA (Senin istediğin kontrol)
    if a_degeri == 0:
        qr_verisi, points, _ = detector.detectAndDecode(frame)
        
        if qr_verisi: # Bir QR kodu yakalandığında
            if qr_verisi in gecerli_sifreler:
                if qr_verisi not in kullanilmis_kodlar:
                    print(f"\n>>> SONUC: {qr_verisi} - GECBILIR!")
                    kullanilmis_kodlar.add(qr_verisi)
                else:
                    print(f"\n>>> SONUC: {qr_verisi} - GECEMEZ (Daha önce kullanıldı!)")
            else:
                print(f"\n>>> SONUC: {qr_verisi} - GECEMEZ (Sistemde yok!)")
            
            # OKUMA YAPILDI: a değerini artır ve sistemi kilitle
            a_degeri += 1 
            print(f"Sistem kilitlendi (a={a_degeri}). Yeni işlem için 'c' tuşuna basın.")

    # Ekranda durumu göster
    durum_metni = "SISTEM: HAZIR ('a' ya bas)" if a_degeri == 0 else "SISTEM: KILITLI ('c' ye bas)"
    renk = (0, 255, 0) if a_degeri == 0 else (0, 0, 255)
    cv2.putText(frame, durum_metni, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, renk, 2)

    cv2.imshow('QR Kontrol Sistemi', frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()