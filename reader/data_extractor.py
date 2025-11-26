from reader.base_reader import BaseReader

class DataExtractor(BaseReader):

    def __init__(self, base_reader: BaseReader):
        self.base_reader = base_reader

    def get_modality(self):
        return self.base_reader.modality_found_final
    

    def get_instrumento(self):
        return self.base_reader.instrumento
    
    
    def get_amparo_legal(self):
        return self.base_reader.amparo_legal


    def get_modo_disputa(self):
        return self.base_reader.modo_disputa
    
    
    def get_type_document(self):
        return self.base_reader.type_doc
    

    def get_code_unity_buy(self):
        return self.base_reader.code_unity_buy