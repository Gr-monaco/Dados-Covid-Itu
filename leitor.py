try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2  
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


f = open('saidas.txt', 'w')

for i in range(16, 72):
    print('Imagem ', str(i))
    original = cv2.imread('C:/Users/gr-mo/PycharmProjects/Dados-Covid-Itu/ImagensAlteradas/imagem' + str(i) +'.jpeg')
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    ret, original2 = cv2.threshold(original, 100, 255, cv2.THRESH_BINARY)
    # scale_percent = 200  # percent of original size
    # width = int(original2.shape[1] * 300 / 100)
    # height = int(original2.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # original2 = cv2.resize(original2, dim, interpolation=cv2.INTER_AREA)
    recorte = original2[250:350, 690:980]
    leitura = pytesseract.image_to_string(recorte, config="-c tessedit_char_whitelist=0123456789% --psm 13 --oem 3  ")
    print(leitura)
    limpo = ''.join(i for i in leitura if i.isdigit())
    f.write(str(i) + ' ' + limpo + '\n')

f.close()
