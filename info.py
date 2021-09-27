import cv2 as cv


nome_imagem = 'imagens/imagem'
f = open('tamanhos.txt', 'w')


def abrir_arquivo(nome, extensao):
    try:
        imagem = cv.imread(nome + extensao)
        height, width, channels = imagem.shape
        f.writelines(f'Imagem {i}: Largura :{width} Altura: {height}\n')

    except AttributeError:
        print(f'{nome + extensao} não existe!')
        if extensao == '.jpeg':
            print('Tentando .jpg')
            abrir_arquivo(nome, '.jpg')
    print('')


for i in range(16, 383):
    nome_imagem_completa = nome_imagem + str(i)
    print(nome_imagem_completa)
    abrir_arquivo(nome_imagem_completa, '.jpeg')

