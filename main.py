from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# JSON dosyasını yükle
with open("ipdata.json") as f:
    ip_database = json.load(f)

@app.route('/')
def index():
    return '''
    <h2>81 İl İçin IP Listesi</h2>
    <form action="/get_ips" method="post">
        Şehir Adı (küçük harf): <input type="text" name="city">
        <input type="submit" value="Göster">
    </form>
    '''

@app.route('/get_ips', methods=['POST'])
def get_ips():
    city = request.form.get("city", "").lower()
    if city in ip_database:
        ip_list = ip_database[city]
        return f"<h3>{city.upper()} için IP Adresleri:</h3><pre>{json.dumps(ip_list, indent=2)}</pre>"
    else:
        return "<h3>Şehir bulunamadı. Lütfen geçerli bir şehir girin.</h3>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
