class Parametro:
    intervalo_de_imagem = []
    intervalo_de_area = []
    conjunto_de_intervalos = []
    configuracao = '--psm 13 --oem 3'

    def __init__(self, intervalo_de_imagem=None, intervalo_de_area=None):
        if intervalo_de_area is None:
            intervalo_de_area = []
        if intervalo_de_imagem is None:
            intervalo_de_imagem = []
        self.intervalo_de_imagem = intervalo_de_imagem
        self.intervalo_de_area = intervalo_de_area

    def adiciona_intervalo(self, lista_de_intervalos: list):
        intervalos_ = len(lista_de_intervalos)
        for i in range(intervalos_-1):
            intervalo_a_adicionar = [lista_de_intervalos[i], lista_de_intervalos[i + 1]]
            self.intervalo_de_imagem.append(intervalo_a_adicionar)
            if i == intervalos_-2:
                self.intervalo_de_imagem.append([lista_de_intervalos[i + 1]])

        return self

    def adiciona_intervalo_de_area(self, lista_de_area):
        # a lista é uma lista de listas
        #
        #[
        #   [[1, 2], [3, 4]],
        #   [[5, 6], [7, 8]]
        #]
        #
        self.intervalo_de_area = lista_de_area
        return self

    def seleciona_configuracao(self, config: str):
        self.configuracao = config
        return self


    def finaliza(self):
        self.conjunto_de_intervalos = [self.intervalo_de_imagem, self.intervalo_de_area]

