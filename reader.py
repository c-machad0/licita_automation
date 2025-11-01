from pypdf import PdfReader
from config import MODALITIES, RELACIONAMENTOS


class Register:
    def __init__(self):
        self.reader = PdfReader('03. CONTRATO GASES MEDICINAIS - ITAOX.pdf')
        self.page = self.reader.pages[0]
        self.text = self.page.extract_text()

        # Dividir o texto em linhas
        self.lines = self.text.split('\n')

        self.modality_found = None
        self.modality_found_dict = None
        self.instrumento = None
        self.modo_disputa = None


    def read_doc(self):
        self.read_modality = None

        # Encontrado a modalidade através do texto lido
        for line in self.lines:
            for modalidade in MODALITIES:
                if modalidade in line:
                    self.read_modality = modalidade
                    break
        
        return self.read_modality.lower()


    def write_field(self):
        num_modalidade = self.lines[10][-9:]
        num_processo = self.lines[11][-9:]
        objeto = self.lines[36] + self.lines[37] + self.lines[38]

        info_bid = {
            'Número da Compra': num_modalidade,
            'Ano da Compra': 2025,
            'Execução': 'Prefeitura Municipal de Itajuípe',
            'Certame': 'Prefeitura Municipal de Itajuípe',
            'PA': num_processo,
            'Objeto': objeto 
        }

        return info_bid

    def select_field(self):
        # Verifica se modality_bid é uma string e não vazia
        if not self.read_modality or not isinstance(self.read_modality, str):
            raise ValueError("Valor inválido em read_modality")

        if self.read_modality is None:
            raise ValueError("Modalidade não encontrada no texto")

        for i in RELACIONAMENTOS: # Itera sobre todo dicionário
            for j in RELACIONAMENTOS['Modalidade'].keys(): # Itera sobre cada modalidade. Ex: Dispensa, Inex, Pregão
                if self.read_modality.lower() in j.lower(): # Captura o nome da modalidade desejada
                    self.modality_found_dict = j # armazena a modalidade encontrada no dicionario em uma variável
                    break

        if self.modality_found_dict is None:
            raise ValueError("Modalidade não encontrada no RELACIONAMENTOS")
        

        # Extrai lista de instrumentos e modo de disputa correspondentes
        instrumentos = RELACIONAMENTOS['Modalidade'][self.modality_found_dict].get('Instrumento', [])
        modos_disputa = RELACIONAMENTOS['Modalidade'][self.modality_found_dict].get('Modo de Disputa', [])

        self.instrumento = instrumentos[0] if instrumentos else None
        self.modo_disputa = modos_disputa[0] if modos_disputa else None

    def get_modality(self):
        return self.modality_found_dict
    
    def get_instrumento(self):
        return self.instrumento
    
    def get_modo_disputa(self):
        return self.modo_disputa


if __name__ == '__main__':
    teste = Register()
    name = teste.read_doc()
    teste.select_field()

    print(name)
    print(teste.get_modality(), teste.get_instrumento(), teste.get_modo_disputa())
"""
Captação de n° de dispensa e processo adm: por meio dos 8 primeiros caracteres, fazendo de ordem inversa
N° da modalidade estará na linha 10
N° do PA estará na linha 11
N° do objeto da linha 36 a 38
"""