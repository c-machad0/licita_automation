import pandas as pd

from reader.base_reader import BaseReader
from utils import find_file_in_directory, extract_all_items

class ExcelProcessor(BaseReader):
    
    def read_spreadsheet(self):
        filepath = find_file_in_directory(self.directory, 'Itens')
        if not filepath:
            raise FileNotFoundError("Arquivo não encontrado.")
        df = pd.read_excel(filepath)
        return extract_all_items(df)