import socket
import threading
import datetime
import subprocess
import whois
import requests

PORT = 2222  # SSH benzeri port

def os_tahmini(ip):
    try:
        # Ping ile TTL değerini al
        result = subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.DEVNULL).decode()
        for line in result.split("\n"):
            if "ttl=" in line.lower():
                ttl_value = int(line.lower().split("ttl=")[1].split()[0])
                if ttl_value <= 64:
                    return "Linux/macOS (TTL=%d)" % ttl_value
                elif ttl_value <= 128:
                    return "Windows (TTL=%d)" % ttl_value
                elif ttl_value <= 255:
                    return "Cisco/Ağ Cihazı (TTL=%d)" % ttl_value
        return "OS tahmin edilemedi"
    except:
        return "TTL alınamadı"

def whois_bilgisi(ip):
    try:
        bilgi = whois.whois(ip)
        domain = bilgi.domain_name
        org = bilgi.org
        if isinstance(domain, list):
            domain = domain[0]
        return f"WHOIS: {domain or 'Domain bulunamadı'} | {org or 'Organizasyon bilinmiyor'}"
    except Exception as e:
        return f"WHOIS alınamadı: {str(e)}"

def ip_konum_bilgisi(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,query"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data["status"] == "success":
            return f"{data['country']} / {data['regionName']} / {data['city']} (IP: {data['query']})"
        else:
            return "Konum bilgisi alınamadı."
    except Exception as e:
        return f"Konum bilgisi alınamadı: {str(e)}"

def handle_client(client_socket, addr):
    ip = addr[0]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n[{time}] ⚠️ Yeni bağlantı alındı!")
    print(f"[+] IP Adresi: {ip}")
    print("[+] OS Tahmini:", os_tahmini(ip))
    print("[+] WHOIS Bilgisi:", whois_bilgisi(ip))
    print("[+] IP Konum Bilgisi:", ip_konum_bilgisi(ip))

    try:
        client_socket.send(b"SSH-2.0-OpenSSH_7.9p1 Ubuntu-10\n")
        while True:
            command = client_socket.recv(1024)
            if not command:
                break
            decoded = command.decode(errors="ignore").strip()
            print(f"[{ip}] Girdi: {decoded}")
            client_socket.send(b"Komut anlaşılamadı.\n")
    except Exception as e:
        print(f"[{ip}] Hata: {str(e)}")
    finally:
        client_socket.close()
        print(f"[{ip}] Bağlantı kapatıldı.")

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"[+] Honeypot başlatıldı. Port: {PORT}")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_honeypot()
