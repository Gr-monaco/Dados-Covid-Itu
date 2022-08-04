try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

# https://muthu.co/all-tesseract-ocr-options/ <- Link para todos os parametros de tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

CONFIG_NUMERO = "-c tessedit_char_whitelist=0123456789 --psm 13 --oem 3"


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
    if 16 <= numero <= 38:
        retorno = pytesseract.image_to_string(imagem, config=CONFIG_NUMERO).rstrip()

    return retorno


f = open('saidas.txt', 'w')

for i in range(16, 48):
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
    leitura_de_casos_descartados = pytesseract.image_to_string(casos_descartados,
                                                               config="-c tessedit_char_whitelist=0123456789 "
                                                                      "--psm 13 --oem 3  ").rstrip()
    # https://github.com/tesseract-ocr/tesseract/issues/2923#issuecomment-598503707 <- Resolveu o problema de não
    #                                                                                  detectar espaços.
    leitura_do_dia = pytesseract.image_to_string(dia_do_boletim,
                                                 config="-c tessedit_char_whitelist="
                                                        "'abcdefghijklmnopqrstuvwxyz '0123456789 "
                                                        "--psm 13 --oem 3  ").rstrip()
    print(leitura_do_dia)
    print(leitura_de_casos_descartados)
    limpo = ''.join(i for i in leitura_de_casos_descartados if i.isdigit())
    f.write(str(i) + ' ' + leitura_do_dia.rstrip() + ' ' + limpo + '\n')

f.close()
