from reader.base_reader import BaseReader

class FieldMapper(BaseReader):
    
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

        for i in self.modality_relations: # Itera sobre todo dicionário
            for j in self.modality_relations['Modalidade'].keys(): # Itera sobre cada modalidade. Ex: Dispensa, Inex, Pregão
                if self.read_modality.lower() in j.lower(): # Captura o nome da modalidade desejada
                    self.modality_found_final = j # armazena a modalidade encontrada no dicionario em uma variável
                    break

        if self.modality_found_final is None:
            raise ValueError("Modalidade não encontrada no RELACIONAMENTOS")
        

        # Extrai lista de instrumentos e modo de disputa correspondentes
        instrumentos = self.modality_relations['Modalidade'][self.modality_found_final].get('Instrumento', [])
        modos_disputa = self.modality_relations['Modalidade'][self.modality_found_final].get('Modo de Disputa', [])

        self.instrumento = instrumentos[0] if instrumentos else None
        self.modo_disputa = modos_disputa[0] if modos_disputa else None

        # Selecionar tipo do documento
        type_document = self.modality_relations['Modalidade'][self.modality_found_final].get('Tipo de Documento', [])
        self.type_doc = type_document[0] if type_document else None

        # Selecionar Código da Und Compradora
        code_unity_buy = self.modality_relations['Modalidade'][self.modality_found_final].get('Código', [])
        self.code_unity_buy = code_unity_buy[0] if code_unity_buy else None