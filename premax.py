import requests
import socket
import time

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"[!] Hata: {e}")
        return None

def get_geo(ip):
    url = f"http://ip-api.com/json/{ip}?fields=66846719"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"[!] API hatası: {e}")
        return None

def print_result(data, domain):
    if data['status'] != 'success':
        print("[!] IP bilgisi alınamadı.")
        return

    print("\nIPGeolocation Tool by Muhammet Atilla")
    print("--" * 30)
    print(f"Target: {domain}")
    print(f"IP: {data['query']}")
    print(f"ASN: {data.get('as', 'N/A')}")
    print(f"City: {data.get('city', 'N/A')}")
    print(f"Country: {data.get('country', 'N/A')}")
    print(f"Country Code: {data.get('countryCode', 'N/A')}")
    print(f"ISP: {data.get('isp', 'N/A')}")
    print(f"Latitude: {data.get('lat', 'N/A')}")
    print(f"Longitude: {data.get('lon', 'N/A')}")
    print(f"Organization: {data.get('org', 'N/A')}")
    print(f"Region: {data.get('regionName', 'N/A')}")
    print(f"Timezone: {data.get('timezone', 'N/A')}")
    print(f"ZIP Code: {data.get('zip', 'N/A')}")
    print(f"Google Maps: https://www.google.com/maps/place/{data.get('lat')},{data.get('lon')},16z")
    print("--" * 30)

if __name__ == "__main__":
    target = input("Alan adı girin (örn: instagram.com): ").strip()
    ip = get_ip(target)

    if ip:
        geo = get_geo(ip)
        if geo:
            print_result(geo, target)
        else:
            print("[!] Konum bilgisi alınamadı.")
    else:
        print("[!] IP alınamadı.")