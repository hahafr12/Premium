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
        import socket
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain)
        conn.settimeout(5)
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        return cert
    except:
        return "SSL sertifikası alınamadı"

def site_info(domain):
    url = f"https://{domain}"
    print(f"[*] Domain: {domain}")
    print(f"[*] IP Adresi: {get_ip(domain)}")
    print(f"\n[*] Whois Bilgisi:")
    print(get_whois(domain))
    print(f"\n[*] HTTP Başlıkları:")
    print(get_headers(url))
    print(f"\n[*] SSL Sertifikası:")
    print(get_ssl_info(domain))
    print(f"\n[*] Robots.txt:")
    print(get_robots(url))

# Kullanım
site_info("roblox.com")
