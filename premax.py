from flask import Flask, session, render_template_string, jsonify, request
import time
import random
import string

app = Flask(__name__)
app.secret_key = 'gizli_bir_anahtar'  # Güvenlik için güçlü bir anahtar kullan!

WAIT_SECONDS = 60  # 1 dakika

# Bekleme sayfası HTML'i
WAIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bekleme Sayfası</title>
    <meta charset="utf-8">
    <script>
        var kodGosterildi = false;
        function kontrolEt() {
            if (kodGosterildi) return;
            fetch('/kod')
                .then(response => response.json())
                .then(data => {
                    if (data.kod) {
                        kodGosterildi = true;
                        document.getElementById('bekle').style.display = 'none';
                        document.getElementById('kod').innerText = data.kod;
                    }
                });
        }
        setInterval(kontrolEt, 5000);
    </script>
</head>
<body>
    <div id="bekle">
        <h1>Lütfen bekleyin...</h1>
        <p>Bu bir bekleme sayfasıdır. 1 dakika beklediğinizde kodunuz burada görünecek.</p>
    </div>
    <h2 id="kod"></h2>
</body>
</html>
"""

def generate_fake_code():
    return 'KOD:' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/')
def index():
    if 'start_time' not in session:
        session['start_time'] = time.time()
    return render_template_string(WAIT_HTML)

@app.route('/kod')
def kod():
    start_time = session.get('start_time', time.time())
    elapsed = time.time() - start_time
    if elapsed >= WAIT_SECONDS:
        if 'kod' not in session:
            session['kod'] = generate_fake_code()
        return jsonify({'kod': session['kod']})
    else:
        return jsonify({'kod': None})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
