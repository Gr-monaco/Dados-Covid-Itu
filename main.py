import shutil

import requests
from bs4 import BeautifulSoup



headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

url = "https://itu.sp.gov.br/boletim-coronavirus-itu-16/"

req = requests.get(url,headers)
soup = BeautifulSoup(req.content, 'html.parser')
imagens = soup.find(class_="mkdf-post-image").find('img')
print(imagens.attrs['src'])
r = requests.get(imagens.attrs['src'],headers, stream=True)

with open("imagens/image.jpeg", "wb") as f:
    r.raw.decode_contet = True
    shutil.copyfileobj(r.raw, f)
