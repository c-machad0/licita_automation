from automation.auth import AutenticationManager
from automation.navigation import NavigationManager
from automation.licitacao import LicitaManager
from automation.itens import ItensManager
from automation.upload import UploadManager
from reader.base_reader import BaseReader
from reader.excel_processor import ExcelProcessor
from reader.field_mapper import FieldMapper
from reader.pdf_processor import PDFProcessor


class MainAutomation():

    def __init__(self):
        # 1. Criar instância base compartilhada para readers
        self.base_reader = BaseReader()
        
        # 2. Criar readers passando base_reader compartilhado
        self.pdf_processor = PDFProcessor(self.base_reader)
        self.field_mapper = FieldMapper(self.base_reader)
        self.excel_processor = ExcelProcessor()
        
        # 3. Criar módulo de automação básico (auth, navigation), porque precisa do driver para os próximos
        self.auth = AutenticationManager()
        self.navigation = NavigationManager(self.auth.driver)
        
        # 4. Processar dados primeiro: cria self.info_bid (usado em LicitaManager)
        self._process_data()
        
        # 5. Criar módulos que usam infobid, passando como parâmetro
        self.licita = LicitaManager(self.auth.driver, self.info_bid)
        self.itens = ItensManager(self.auth.driver)
        self.upload = UploadManager(self.auth.driver)
    

    def _process_data(self):
        # Passo 1: Ler PDF e extrair dados básicos
        self.pdf_processor.read_doc()

        # Passo 2: Mapear campos (depende de read_doc)
        self.field_mapper.select_field()

        # Passo 3: Extrair fundamentação legal (depende de select_field)
        self.pdf_processor.read_extract_to_law()

        # Passo 4: Preparar dados para automação
        self.info_bid = self.field_mapper.write_field()


    def run_script(self):
        # Autenticação
        self.auth.access_url()
        self.auth.login()
        
        # Navegação
        self.navigation.home()
        self.navigation.publicacao_legal()
        self.navigation.indexedicao()
        """self.navigation.nova_licitacao()
        self.licita.inserir_licitacao()
        self.itens.add_item()"""
        
        # Processar licitação
        self.licita.consult_licita()
        
        # Upload
        self.upload.upload_arquivos_licitacao()
        
        # Finalizar
        self.auth.quit_app()

if __name__ == '__main__':
    automation = MainAutomation()
    automation.run_script()