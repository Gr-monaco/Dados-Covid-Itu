import cv2 as cv
import os

lista = os.listdir('imagens')

try:
    lista.remove('.gitignore')
except ValueError:
    print("GitIgnore não achado, continuando")
finally:
    for i in lista:
        imagem_original = cv.imread('imagens/'+i)
        width, height, channels = imagem_original.shape
        print(i,imagem_original.shape)
        nova_imagem = imagem_original.copy()

        if height == 1300 and width == 800:
            nova_imagem = cv.resize(nova_imagem, (1280, 787))

        cv.imwrite('C:/Users/gr-mo/PycharmProjects/Dados-Covid-Itu/ImagensAlteradas/'+str(i) , nova_imagem)
