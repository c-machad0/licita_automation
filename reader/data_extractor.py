from reader.base_reader import BaseReader

class DataExtractor(BaseReader):

    def get_modality(self):
        return self.modality_found_final
    

    def get_instrumento(self):
        return self.instrumento
    
    
    def get_amparo_legal(self):
        return self.amparo_legal


    def get_modo_disputa(self):
        return self.modo_disputa
    
    
    def get_type_document(self):
        return self.type_doc
    

    def get_code_unity_buy(self):
        return self.code_unity_buy