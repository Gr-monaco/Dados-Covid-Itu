try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

# https://muthu.co/all-tesseract-ocr-options/ <- Link para todos os parametros de tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

CONFIG_NUMERO = "-l lato --psm 13 --oem 3 -c tessedit_char_whitelist=0123456789"
CONFIG_TEXTO = "-c tessedit_char_whitelist='abcdefghijklmnopqrstuvwxyz '0123456789 --psm 13 --oem 3 "


def leitura_de_casos_descartados(numero, imagem):
    recorte = imagem[250:350, 690:980]
    if 16 <= numero < 72:
        recorte = imagem[250:350, 690:980]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_NUMERO).rstrip()

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
    retorno = 0
    recorte = imagem[250:350, 160:330]  # valor padrão
    if 16 <= numero <= 38:
        recorte = imagem[250:350, 160:330]
    if 38 < numero <= 72:
        recorte = imagem[250:297, 150:242]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_NUMERO).rstrip()

    return retorno

def leitura_de_data(numero, imagem):
    retorno = "erro"
    recorte = imagem[50:80, 1000:1250]  # valor padrão
    if 16 <= numero <= 48:
        recorte = imagem[50:80, 1000:1250]
    if 48 < numero:
        recorte = imagem[25:60, 1000:1260]

    retorno = pytesseract.image_to_string(recorte, config=CONFIG_TEXTO).rstrip()

    return retorno

f = open('saidas.txt', 'w')

for i in range(16, 72):
    print('Imagem ', str(i))
    original = cv2.imread('C:/Users/gr-mo/PycharmProjects/Dados-Covid-Itu/ImagensAlteradas/imagem' + str(i) + '.jpeg')
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    ret, original2 = cv2.threshold(original, 100, 255, cv2.THRESH_BINARY)
    # scale_percent = 200  # percent of original size
    # width = int(original2.shape[1] * 300 / 100)
    # height = int(original2.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # original2 = cv2.resize(original2, dim, interpolation=cv2.INTER_AREA)
    casos_descartados = original2[250:350, 690:980]
    dia_do_boletim = original2[50:80, 1000:1250]

    # https://docs.python.org/3/library/stdtypes.html#str.rstrip
    casos_descartados_n = leitura_de_casos_descartados(i, original2)
    # https://github.com/tesseract-ocr/tesseract/issues/2923#issuecomment-598503707 <- Resolveu o problema de não
    #                                                                                  detectar espaços.
    leitura_do_dia = leitura_de_data(i, original2)
    casos_confirmados = leitura_de_casos_confirmados(i, original2)
    obitos_confirmados = leitura_de_obitos_confirmados(i, original2)
    print(leitura_do_dia)
    print(casos_confirmados)
    print(obitos_confirmados)
    print("casos des" + casos_descartados_n)
    f.write(str(i) + ' ' + leitura_do_dia.rstrip() + ' ' + casos_descartados_n + ' ' + str(casos_confirmados) + ' ' + obitos_confirmados + '\n')

f.close()
