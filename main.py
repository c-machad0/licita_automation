from automation.auth import AutenticationManager
from automation.navigation import NavigationManager
from automation.licitacao import LicitaManager
from automation.itens import ItensManager
from automation.upload import UploadManager



class MainAutomation(AutenticationManager, NavigationManager, LicitaManager, ItensManager, UploadManager):

    def __init__(self):
        super().__init__()

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