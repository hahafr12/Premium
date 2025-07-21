import socket
import requests
import whois
import json

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return "IP alınamadı"

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return w
    except:
        return "Whois bilgisi alınamadı"

def get_headers(url):
    try:
        response = requests.get(url)
        return response.headers
    except:
        return "HTTP başlıkları alınamadı"

def get_robots(url):
    try:
        response = requests.get(url + "/robots.txt")
        if response.status_code == 200:
            return response.text
        else:
            return "robots.txt bulunamadı"
    except:
        return "robots.txt alınamadı"

def get_ssl_info(domain):
    try:
        import ssl
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(5)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        return cert
    except:
        return "SSL sertifikası alınamadı"

def main():
    print("🔎 Web Site Bilgi Toplama Aracı")
    domain = input("Lütfen alan adını girin (örnek: roblox.com): ").strip()

    if not domain:
        print("Alan adı boş olamaz!")
        return

    url = "https://" + domain
    print("\n--- Sonuçlar ---")
    print(f"[✓] Domain: {domain}")
    print(f"[✓] IP Adresi: {get_ip(domain)}")

    print("\n[✓] Whois Bilgisi:")
    print(get_whois(domain))

    print("\n[✓] HTTP Başlıkları:")
    headers = get_headers(url)
    if isinstance(headers, dict):
        for key, value in headers.items():
            print(f"{key}: {value}")
    else:
        print(headers)

    print("\n[✓] SSL Sertifikası:")
    ssl_info = get_ssl_info(domain)
    if isinstance(ssl_info, dict):
        print(json.dumps(ssl_info, indent=2))
    else:
        print(ssl_info)

    print("\n[✓] Robots.txt Dosyası:")
    print(get_robots(url))

if __name__ == "__main__":
    main()
