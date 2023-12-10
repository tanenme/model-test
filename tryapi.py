import requests

resp = requests.post("https://getpredict-wvu4btzfga-et.a.run.app/", files={'file': open('400.jpg', 'rb')})

print(resp.json())