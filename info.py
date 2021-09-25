from PIL import Image

f = open('tamanhos.txt', 'w')
nome_imagem = 'imagens/imagem'


def abrir_arquivo(nome, extensao):
    try:
        imagem = Image.open(nome + extensao)
        width, height = imagem.size
        f.writelines(f'Imagem {i}: Largura :{width} Altura: {height}\n')

    except FileNotFoundError:
        print(f'{nome_imagem_completa + extensao} não existe!')
        if extensao == '.jpeg':
            print('Tentando .jpg')
            abrir_arquivo(nome, '.jpg')
    print('')


for i in range(16, 383):
    nome_imagem_completa = nome_imagem + str(i)
    print(nome_imagem_completa)
    abrir_arquivo(nome_imagem_completa, '.jpeg')

