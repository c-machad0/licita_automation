from automation.auth import AutenticationManager
from automation.navigation import NavigationManager
from automation.licitacao import LicitaManager
from automation.itens import ItensManager
from automation.upload import UploadManager
from reader.base_reader import BaseReader
from reader.excel_processor import ExcelProcessor
from reader.field_mapper import FieldMapper
from reader.pdf_processor import PDFProcessor


class MainAutomation(AutenticationManager, NavigationManager, LicitaManager, ItensManager, UploadManager):

    def __init__(self):
        super().__init__() # Inicializa BaseAutomation

        # Inicializando os readers
        self.base_reader = BaseReader()
        self.pdfprocessor = PDFProcessor()
        self.excelprocessor = ExcelProcessor()
        self.fieldmapper = FieldMapper()

        self.pdfprocessor.read_doc()
        self.fieldmapper.select_field()
        self.pdfprocessor.read_extract_to_law()
        self.infobid = self.fieldmapper.write_field()

    def run_script(self):
        self.access_url()
        self.login()
        self.home()
        self.publicacao_legal()
        self.indexedicao()

        self.consult_licita()
        self.upload_arquivos_licitacao()
        self.quit_app()
        """
        else:
            print('Não existe. Programa continuando')
            self.nova_licitacao()
            self.inserir_compra()
            self.upload_arquivos_licitacao()
            self.quit_app()
        """

if __name__ == '__main__':
    automation = MainAutomation()
    automation.run_script()