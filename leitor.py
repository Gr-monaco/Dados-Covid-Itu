import pandas as pd
import os
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
from ConstrutorDeParametro import Parametro

# https://github.com/tesseract-ocr/tesseract/issues/2923#issuecomment-598503707 <- Resolveu o problema de não
#                                                                                  detectar espaços.
# https://docs.python.org/3/library/stdtypes.html#str.rstrip
# Ver o paddle https://github.com/PaddlePaddle/PaddleOCR
# https://muthu.co/all-tesseract-ocr-options/ <- Link para todos os parametros de tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

CONFIG_NUMERO = "-l lato --psm 13 --oem 3 -c tessedit_char_whitelist=0123456789"
CONFIG_TEXTO = "--psm 13 --oem 3 -c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyz 0123456789'  "


def acha_mes(data: str):
    listademes = ['janeiro',
                  'fevereiro',
                  'mar',
                  'abril',
                  'maio',
                  'junho',
                  'julho',
                  'agosto',
                  'setembro',
                  'outubro',
                  'novembro',
                  'dezembro']

    for mes in listademes:
        if mes in data:
            return "{:02d}".format(listademes.index(mes) + 1)


def limpeza(rec):
    contours, hierarchy = cv2.findContours(rec, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    stencil = np.zeros(rec.shape).astype(rec.dtype)
    ROI = []
    for con in contours:
        x, y, w, h = cv2.boundingRect(con)
        if (h > 20):
            ROI.append(con)

    for con in ROI:
        x, y, w, h = cv2.boundingRect(con)
        roi = rec[y:y + h, x:x + w]

        stencil[y:y + h, x:x + w] = roi

    return stencil


def leitura(numero: int, imagem, parametros: Parametro):
    for i in range(len(parametros.intervalo_de_imagem)):
        if len(parametros.intervalo_de_imagem[i]) == 1:
            if numero > parametros.intervalo_de_imagem[i][0]:
                dados_de_area = parametros.intervalo_de_area[-1]
                parte = imagem[dados_de_area[0][0]:dados_de_area[0][1],
                        dados_de_area[1][0]:dados_de_area[1][1]]
                limpo = limpeza(parte)

                return pytesseract.image_to_string(limpo, config=parametros.configuracao).rstrip()  # pega ultimo conjunto

        if parametros.intervalo_de_imagem[i][0] < numero <= parametros.intervalo_de_imagem[i][1]:
            dados_de_area = parametros.intervalo_de_area[i]
            parte = imagem[dados_de_area[0][0]:dados_de_area[0][1],
                    dados_de_area[1][0]:dados_de_area[1][1]]
            limpo = limpeza(parte)

            return pytesseract.image_to_string(limpo, config=parametros.configuracao).rstrip()  # pega ultimo conjunto

    pass


def leitura_de_casos_descartados(numero, imagem):
    recorte = imagem[250:350, 700:985]  # funciona bem para 4 digitos

    contours, hierarchy = cv2.findContours(recorte, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    stencil = np.zeros(recorte.shape).astype(imagem.dtype)
    ROI = []
    for con in contours:
        if 300 <= cv2.contourArea(con):
            ROI.append(con)  # ROI

    for con in ROI:
        x, y, w, h = cv2.boundingRect(con)
        roi = recorte[y:y + h, x:x + w]

        stencil[y:y + h, x:x + w] = roi

    retorno = pytesseract.image_to_string(stencil, config=CONFIG_NUMERO).rstrip()

    return retorno


def leitura_de_obitos_confirmados(numero, imagem):
    recorte = imagem[610:715, 690:860]
    if 16 <= numero < 72:
        recorte = imagem[610:715, 690:860]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_NUMERO).rstrip()

    return retorno


def leitura_de_casos_confirmados(numero, imagem):
    """
    Faz a leitura do numero de casos confirmados.
    Dependendo do numero da imagem, a leitura é feita em um trecho diferente. Este comportamento
    ainda é hardcoded.
    @rtype: int
    @param numero: numero da imagem sendo analizada
    @param imagem: imagem a ser analizada
    """
    recorte = imagem[250:350, 160:330]  # valor padrão
    if 16 <= numero <= 38:
        recorte = imagem[250:350, 160:330]
    if 38 < numero <= 72:
        recorte = imagem[250:297, 150:242]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_NUMERO).rstrip()

    return retorno


def leitura_de_data(numero, imagem):
    recorte = imagem[50:80, 1000:1250]  # valor padrão
    if 16 <= numero <= 48:
        recorte = imagem[50:80, 1000:1250]
    if 48 < numero:
        recorte = imagem[25:63, 990:1260]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_TEXTO).rstrip()

    return retorno


coluna_numero_imagem = np.array([])
coluna_dia = np.array([])
coluna_casos_confirmados = np.array([])
coluna_obitos_confirmados = np.array([])
coluna_casos_descartados = np.array([])

params_casos_conf = Parametro()
params_casos_conf.adiciona_intervalo([15, 38, 71]).adiciona_intervalo_de_area([
    [[250, 360], [150, 650]],
    [[250, 300], [150, 650]],
    [[225, 265], [150, 620]]
]).seleciona_configuracao("-l lato --psm 13 --oem 3 -c tessedit_char_whitelist=0123456789").finaliza()


params_obitos_conf = Parametro()
params_obitos_conf.adiciona_intervalo([15, 71, 222]).adiciona_intervalo_de_area([
    [[610, 720], [690, 1180]],
    [[505, 600], [665, 1130]],
    [[505, 600], [150, 615]]
]).seleciona_configuracao("-l lato --psm 13 --oem 3 -c tessedit_char_whitelist=0123456789").finaliza()

for i in range(16, 502):
    if not os.path.exists('C:/Users/gr-mo/PycharmProjects/Dados-Covid-Itu/ImagensAlteradas/imagem' + str(i) + '.jpeg'):
        continue
    if i == 142 or i == 393:
        continue
    print('Imagem ', str(i))
    original = cv2.imread('C:/Users/gr-mo/PycharmProjects/Dados-Covid-Itu/ImagensAlteradas/imagem' + str(i) + '.jpeg')
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    ret, original2 = cv2.threshold(original, 170, 255, cv2.THRESH_BINARY)
    # scale_percent = 200  # percent of original size

    # width = int(original2.shape[1] * 300 / 100)
    # height = int(original2.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # original2 = cv2.resize(original2, dim, interpolation=cv2.INTER_AREA)
    casos_descartados = original2[250:350, 690:980]
    dia_do_boletim = original2[50:80, 1000:1250]

    leitura_do_dia = leitura_de_data(i, original2).replace(" ", "")
    print("RAW: ", leitura_do_dia)
    leitura_do_dia = leitura_do_dia[0:2] + '/' + acha_mes(leitura_do_dia) + '/' + leitura_do_dia[-4:]
    casos_confirmados = leitura(i, original2, params_casos_conf)
    coluna_numero_imagem = np.append(coluna_numero_imagem, i)
    coluna_dia = np.append(coluna_dia, leitura_do_dia)
    coluna_casos_confirmados = np.append(coluna_casos_confirmados, casos_confirmados)
    print('Casos confirmados: ', casos_confirmados)
    print('Dia:', leitura_do_dia)

d = {'Numero da Imagem': coluna_numero_imagem,
     'Data': coluna_dia,
     'Casos Confirmados': coluna_casos_confirmados,
     }
df = pd.DataFrame(data=d)

# transforma em tipo int64 para tirar o .0 do numero e dps passa para string
df['Numero da Imagem'] = df['Numero da Imagem'].astype(np.int64).astype('str', errors='raise')
print(df['Numero da Imagem'].dtypes)
print(df)
df.to_excel("output.xlsx")
