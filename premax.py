import socket
import threading
import time

HOST = '0.0.0.0'
PORT = 443

active_clients = {}

# HTML: Bekleme Sayfası
wait_html = """\
HTTP/1.1 200 OK
Content-Type: text/html

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
                .then(response => response.text())
                .then(txt => {
                    if (txt.startsWith('KOD:')) {
                        kodGosterildi = true;
                        document.getElementById('bekle').style.display = 'none';
                        document.getElementById('kod').innerText = txt;
                    }
                });
        }
        setInterval(kontrolEt, 5000);
    </script>
</head>
<body>
    <div id="bekle">
        <h1>Lütfen bekleyin...</h1>
        <p>Bu bir bekleme sayfasıdır. 10 dakika beklediğinizde kodunuz burada görünecek.</p>
    </div>
    <h2 id="kod"></h2>
</body>
</html>
"""

def generate_fake_code():
    import random, string
    return 'KOD:' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def client_thread(conn, addr):
    first_request_time = time.time()
    session_id = str(addr)
    active_clients[session_id] = first_request_time

    try:
        while True:
            request = conn.recv(1024)
            if not request:
                break
            request_line = request.decode().split('\r\n')[0]
            print(f"[{addr}] İstek: {request_line}")

            if request_line.startswith('GET /kod'):
                elapsed = time.time() - active_clients[session_id]
                if elapsed >= 600:  # 10 dakika
                    fake_code = generate_fake_code()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{fake_code}"
                else:
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBekleniyor..."
                conn.sendall(response.encode('utf-8'))
            else:
                conn.sendall(wait_html.encode('utf-8'))
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        conn.close()
        if session_id in active_clients:
            del active_clients[session_id]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Sunucu {PORT} portunda başlatıldı.")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_thread, args=(conn, addr), daemon=True).start()