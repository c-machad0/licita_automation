from pypdf import PdfReader
from config import MODALITIES, RELACIONAMENTOS, DEFAULT_DIRECTORY
from utils import find_file_in_directory

class Register:
    def __init__(self):
        self.reader = PdfReader(find_file_in_directory(DEFAULT_DIRECTORY, 'Contrato'.upper()))
        self.page = self.reader.pages[0]
        self.text = self.page.extract_text()

        # Dividir o texto em linhas
        self.lines = self.text.split('\n')

        self.modality_found = None
        self.modality_found_dict = None
        self.instrumento = None
        self.modo_disputa = None


    def read_doc(self):
        """
        Função que extrai os dados necessários do texto. [modalidade, numero da modalidade,
        numero do processo administrativo e objeto]
        """

        self.read_modality = None
        self.read_num_modality = None
        self.read_admprocess = None
        self.read_object = None
        self.type_doc = None
        self.code_unity_buy = None

        # Encontrado a modalidade e seu numero através do texto lido
        for index, line in enumerate(self.lines):
            for modalidade in MODALITIES:
                if modalidade in line:
                    self.read_modality = modalidade # Armazenando a modalidade em read_modality
                    self.read_num_modality = self.lines[index][-9:] # Armazenando o numero da modalidade em read_num_modality
                    break
        
        # Encontrar numero do processo adminstrativo
        for line in self.lines:
            if 'Processo Administrativo'.upper() in line:
                # PROCESSO ADMMINISTRATIVO N° 
                self.read_admprocess = line[-9:]
                break
        
        result_lines = []
        found = False

        # Encontrar objeto
        for line in self.lines:
            if 'Objeto'.upper() in line.upper():
                found = True
                continue
            if found:
                if line.strip() == '':
                    break
                result_lines.append(line)
        
        self.read_object = ''.join(result_lines)

        return f'{self.read_modality.lower()} {self.read_num_modality} - Processo Administrativo: {self.read_admprocess} \nObjeto: {self.read_object}'


    def write_field(self):

        info_bid = {
            'Número da Compra': self.read_num_modality,
            'Ano da Compra': 2025,
            'Execução': 'Prefeitura Municipal de Itajuípe',
            'Certame': 'Prefeitura Municipal de Itajuípe',
            'PA': self.read_admprocess,
            'Objeto': self.read_object 
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

        # Selecionar tipo do documento
        type_document = RELACIONAMENTOS['Modalidade'][self.modality_found_dict].get('Tipo de Documento', [])
        self.type_doc = type_document[0] if type_document else None

        # Selecionar Código da Und Compradora
        code_unity_buy = RELACIONAMENTOS['Modalidade'][self.modality_found_dict].get('Código', [])
        self.code_unity_buy = code_unity_buy[0] if code_unity_buy else None


    def get_modality(self):
        return self.modality_found_dict
    

    def get_instrumento(self):
        return self.instrumento
    

    def get_modo_disputa(self):
        return self.modo_disputa
    
    
    def get_type_document(self):
        return self.type_doc
    

    def get_code_unity_buy(self):
        return self.code_unity_buy


if __name__ == '__main__':
    teste = Register()
    name = teste.read_doc()
    teste.select_field()

    print(name.title())
    print(teste.get_modality(), teste.get_instrumento(), teste.get_modo_disputa(), teste.get_code_unity_buy(), teste.get_type_document())
"""
Captação de n° de dispensa e processo adm: por meio dos 8 primeiros caracteres, fazendo de ordem inversa
N° da modalidade estará na linha 10
N° do PA estará na linha 11
N° do objeto da linha 36 a 38
"""