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
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        imagens_raw = soup.find(class_="mkdf-post-image")
        if imagens_raw is None:
            imagens = soup.find(class_="mkdf-post-text-inner").find('img')
            r = requests.get(imagens.attrs['srcset'], headers, stream=True)
            ultima_https = imagens['srcset'].rfind('https:')
            ultima_jpg = imagens['srcset'].rfind('jpeg')
            print(ultima_https, ultima_jpg)
            print(imagens['srcset'][ultima_https:ultima_jpg+4])
        else:
            imagens = imagens_raw.find('img')
            r = requests.get(imagens.attrs['src'], headers, stream=True)

        pasta = "imagens/imagem" + str(index) + ".jpeg"
        with open(pasta, "wb") as f:
            r.raw.decode_contet = True
            shutil.copyfileobj(r.raw, f)

        timer = random.randint(10, 30)
        print(f'Esperando {timer} segundos antes de ir para proximo URL')
        time.sleep(timer)
        print()
    else:
        print("Página com erro!")


url_incompleto = "https://itu.sp.gov.br/boletim-coronavirus-itu-"

# for i in range(312, 383):
#     url_completo = url_incompleto + str(i) + "/"
#     pegar_imagem(url_completo, i)


url_completo = url_incompleto + str(312) + "/"
pegar_imagem(url_completo, 312)
