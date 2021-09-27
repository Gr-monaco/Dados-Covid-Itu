import cv2 as cv
import os

lista = os.listdir('imagens')
lista.remove('.gitignore')

for i in lista:
    imagem_original = cv.imread('imagens/'+i)
    width, height, channels = imagem_original.shape
    print(imagem_original.shape)
    nova_imagem = imagem_original.copy()

    if height == 1300 and width == 800:
        nova_imagem = cv.resize(nova_imagem, (1280, 787))

    cv.imwrite('ImagemAlteradas/'+str(i) , nova_imagem)
