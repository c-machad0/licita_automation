from reader.base_reader import BaseReader

class FieldMapper(BaseReader):
    
    def __init__(self, base_reader: BaseReader):
        self.base_reader = base_reader
        self.modality_relations = base_reader.modality_relations


    def write_field(self):

        info_bid = {
            'Número da Compra': self.base_reader.read_num_modality,
            'Ano da Compra': 2025,
            'Execução': 'Prefeitura Municipal de Itajuípe',
            'Certame': 'Prefeitura Municipal de Itajuípe',
            'PA': self.base_reader.read_admprocess,
            'Objeto': self.base_reader.read_object 
        }

        return info_bid


    def select_field(self):
        """
        Seleciona campos baseado na modalidade (depende de read_doc).
        """


        # Verifica se modality_bid é uma string e não vazia
        if not self.base_reader.read_modality or not isinstance(self.base_reader.read_modality, str):
            raise ValueError("Valor inválido em read_modality")

        if self.base_reader.read_modality is None:
            raise ValueError("Modalidade não encontrada no texto")

        for i in self.modality_relations: # Itera sobre todo dicionário
            for j in self.modality_relations['Modalidade'].keys(): # Itera sobre cada modalidade. Ex: Dispensa, Inex, Pregão
                if self.base_reader.read_modality.lower() in j.lower(): # Captura o nome da modalidade desejada
                    self.base_reader.modality_found_final = j # armazena a modalidade encontrada no dicionario em uma variável
                    break

        if self.base_reader.modality_found_final is None:
            raise ValueError("Modalidade não encontrada no RELACIONAMENTOS")
        

        # Extrai dados correspondentes
        relacao = self.modality_relations['Modalidade'][
            self.base_reader.modality_found_final
        ]
        
        instrumentos = relacao.get('Instrumento', [])
        modos_disputa = relacao.get('Modo de Disputa', [])
        type_document = relacao.get('Tipo de Documento', [])
        code_unity_buy = relacao.get('Código', [])
        
        self.base_reader.instrumento = instrumentos[0] if instrumentos else None
        self.base_reader.modo_disputa = modos_disputa[0] if modos_disputa else None
        self.base_reader.type_doc = type_document[0] if type_document else None
        self.base_reader.code_unity_buy = code_unity_buy[0] if code_unity_buy else None