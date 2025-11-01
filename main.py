import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager


from config import URLS, LOGIN, DEFAULT_DIRECTORY
from reader import Register


class Automation:
    def __init__(self):
        self.default_dir = DEFAULT_DIRECTORY
        self.options = Options()
        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.maximize_window() # Fazer com que as janelas sempre sejam maximizadas


    # Orquestrador
    def run_script(self):
        self.access_url()
        self.login()
        self.home()
        self.publicacao_legal()
        self.indexedicao()
        self.nova_licitacao()
        self.inserir_compra()
        self.quit_app()


    def access_url(self):
        self.driver.get(URLS[0])


    # /Account/Login
    def login(self):
        text_field = self.driver.find_elements(By.CSS_SELECTOR, 'main.login .box form .input input')

        user_input = text_field[0]
        password_input = text_field[1]

        user_input.send_keys(LOGIN['user'])
        password_input.send_keys(LOGIN['password'])

        if user_input and password_input:
            button_login = self.driver.find_element(By.CSS_SELECTOR, 'main.login .box form button, main.login .box form input[type="submit"]')
            button_login.click()

        time.sleep(5)
    

    # /home
    def home(self):
        try:
            # Espera até o botão "Fechar" aparecer e estar clicável
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='close']/a"))
            )

            close_button.click()
           
        except:
            pass
        
        button_publicacoes = self.driver.find_element(By.CSS_SELECTOR, '#main > li:nth-child(5) > a')
        button_publicacoes.click()

        time.sleep(5)


    # /publicacaolegal
    def publicacao_legal(self):
        try:
            button_publicidade = self.driver.find_element(By.CSS_SELECTOR, '#main-menu > div > ul > li:nth-child(1) > a')
            button_publicidade.click()
            print('"Publicidade no Portal" clicado')

        except Exception as e:
            print(f'{e}: Erro ao encontrar o seletor')


    # /sai/enviodom/indexedicao
    def indexedicao(self):
        try:
            button_licitacoes = self.driver.find_element(By.XPATH, '//*[@id="main-menu"]/div/ul/li[22]/a')
            button_licitacoes.click()
            print('"Licitações/Contratações" clicado')

            time.sleep(5)

        except Exception as e:
            print(f'{e}: Erro ao encontrar o seletor')


    # /sai/licitacaocontrato/index
    def nova_licitacao(self):
        try:
            botao = self.driver.find_element(By.LINK_TEXT, 'Nova licitação / contratação (Lei 14.133/21)')
            botao.click()

            print('"Nova Licitação" clicado')

            time.sleep(5)

        except Exception as e:
            print(f'{e}: Erro ao encontrar seletor')


    # /sai/ConfiguracaoPncp/InserirCompra
    def inserir_compra(self):
        register = Register()
        # select_field() popula os atributos self.modality_found_dict, self.instrumento e self.modo_disputa.
        # Os métodos getter acessam esses atributos.
        register.read_doc()
        register.select_field()
        info_bid = register.write_field()

        try:
            # modalidade
            select_modalidade = self.driver.find_element(By.ID, 'compra_ModalidadeId')
            modalidade_select = Select(select_modalidade)
            modalidade_select.select_by_visible_text(register.get_modality())

            print('Opção de modalidade selecionada')

            time.sleep(1)

            # instrumento
            select_instrumento = self.driver.find_element(By.ID, 'compra_TipoInstrumentoConvocatorioId')
            instrumento_select = Select(select_instrumento)
            instrumento_select.select_by_visible_text(register.get_instrumento())

            print('Opção de instrumento selecionada')

            time.sleep(1)

            # modo de disputa
            select_modo = self.driver.find_element(By.ID, 'compra_ModoDisputaId')
            modo_select = Select(select_modo)
            modo_select.select_by_visible_text(register.get_modo_disputa())

            print('Opção de modo selecionada')

            time.sleep(1)

            # n° da modalidade. ex: 027/2025
            field_num_modalidade = self.driver.find_element(By.ID, 'compra_NumeroCompra')
            field_num_modalidade.send_keys(info_bid['Número da Compra'])

            print('N° da modalidade escrito')

            # ano
            field_num_ano = self.driver.find_element(By.ID, 'compra_AnoCompra')
            field_num_ano.send_keys(info_bid['Ano da Compra'])

            print('Ano escrito')

            # local de execução
            field_local_execução = self.driver.find_element(By.ID, 'compra_des_local_execucao_lic')
            field_local_execução.send_keys(info_bid['Execução'])

            print('Local de execução escrito')

            # local do certame
            field_local_certame = self.driver.find_element(By.ID, 'compra_des_local_certame')
            field_local_certame.send_keys(info_bid['Certame'])

            print('Local de certame escrito')

            # local processo administrativo
            field_pa = self.driver.find_element(By.ID, 'compra_NumeroProcesso')
            field_pa.send_keys(info_bid['PA'])

            print('Local do Processo Adm escrito')

            time.sleep(5)

        except Exception as e:
            print(f'{e}: Algum erro encontrado')

    def quit_app(self):
        self.driver.quit()
        

if __name__ == '__main__':
    auto = Automation()
    auto.run_script()