import shutil
import time
import requests
import random
from bs4 import BeautifulSoup

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


def pegar_imagem(url, index):
    print(f'{index} url: {url}')
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    imagens = soup.find(class_="mkdf-post-image").find('img')
    print(imagens.attrs['src'])
    r = requests.get(imagens.attrs['src'], headers, stream=True)

    pasta = "imagens/imagem" + str(index) + ".jpeg"
    with open(pasta, "wb") as f:
        r.raw.decode_contet = True
        shutil.copyfileobj(r.raw, f)

    timer = random.randint(5, 10)
    print(f'Esperando {timer} segundos antes de ir para proximo URL')
    time.sleep(timer)
    print()
    

url_incompleto = "https://itu.sp.gov.br/boletim-coronavirus-itu-"

for i in range(16, 29):
    url_completo = url_incompleto + str(i) + "/"
    pegar_imagem(url_completo, i)



