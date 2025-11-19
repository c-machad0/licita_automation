import time
from datetime import date, datetime

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
from utils import find_file_in_directory, fill_datetime_field, extract_all_items, normalize_select_option_item

class Automation:
    def __init__(self):
        self.default_dir = DEFAULT_DIRECTORY
        self.options = Options()

        prefs = {
            "download.default_directory": self.default_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }

        self.options.add_experimental_option("prefs", prefs)

        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.maximize_window() # Fazer com que as janelas sempre sejam maximizadas

        self.register = Register()
        # select_field() popula os atributos self.modality_found_dict, self.instrumento e self.modo_disputa.
        # Os mtodos getter acessam esses atributos.
        self.register.read_doc()
        self.register.select_field()
        self.register.read_extract_to_law()
        self.info_bid = self.register.write_field()
        
    # Orquestrador
    def run_script(self):
        self.access_url()
        self.login()
        self.home()
        self.publicacao_legal()
        self.indexedicao()

        if self.consult_licita():
            self.quit_app()
        else:
            print('Não existe. Programa continuando')
            self.nova_licitacao()
            self.inserir_compra()
            self.quit_app()


    def access_url(self):
        self.driver.get(URLS[0])


    def consult_licita(self):
        field_numero_licita = self.driver.find_element(By.ID, 'search_NumeroLicitacao')
        field_numero_licita.send_keys(self.info_bid['Número da Compra'])

        field_numero_processo = self.driver.find_element(By.ID, 'search_NumeroProcesso')
        field_numero_processo.send_keys(self.info_bid['PA'])

        # Busca por todas as células (td) que contenham esse número de licitação
        page_elements_licita = self.driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.info_bid['Número da Compra']}')]")

        # Se encontrar 1 ou mais elementos, retorna que existe
        return len(page_elements_licita) > 0


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

        try:
            # modalidade
            select_modalidade = self.driver.find_element(By.ID, 'compra_ModalidadeId')
            modalidade_select = Select(select_modalidade)
            modalidade_select.select_by_visible_text(self.register.get_modality())

            print('Opção de modalidade selecionada')

            time.sleep(1)

            # instrumento
            select_instrumento = self.driver.find_element(By.ID, 'compra_TipoInstrumentoConvocatorioId')
            instrumento_select = Select(select_instrumento)
            instrumento_select.select_by_visible_text(self.register.get_instrumento())

            print('Opção de instrumento selecionada')

            time.sleep(1)

            select_amparo_legal = self.driver.find_element(By. ID, 'compra_AmparoLegalId')
            amparo_legal_select = Select(select_amparo_legal)
            amparo_legal_select.select_by_visible_text(self.register.get_amparo_legal())
            
            print('Opção de amparo legal selecionada')

            time.sleep(1)

            # modo de disputa
            select_modo = self.driver.find_element(By.ID, 'compra_ModoDisputaId')
            modo_select = Select(select_modo)
            modo_select.select_by_visible_text(self.register.get_modo_disputa())

            print('Opção de modo selecionada')

            time.sleep(1)

            # n° da modalidade. ex: 027/2025
            field_num_modalidade = self.driver.find_element(By.ID, 'compra_NumeroCompra')
            field_num_modalidade.send_keys(self.info_bid['Número da Compra'])

            print('N° da modalidade escrito')

            # ano
            field_num_ano = self.driver.find_element(By.ID, 'compra_AnoCompra')
            field_num_ano.send_keys(self.info_bid['Ano da Compra'])

            print('Ano escrito')

            # local de execução
            field_local_execução = self.driver.find_element(By.ID, 'compra_des_local_execucao_lic')
            field_local_execução.send_keys(self.info_bid['Execução'])

            print('Local de execução escrito')

            # local do certame
            field_local_certame = self.driver.find_element(By.ID, 'compra_des_local_certame')
            field_local_certame.send_keys(self.info_bid['Certame'])

            print('Local de certame escrito')

            # Inicializando as variáveis que capturam datas
            start_date_field, _ = self.register.read_notice()
            _, end_date_field = self.register.read_notice()
            contract_date = self.register.read_extract_to_time()

            # Chamando função auxiliar para adicionar datas
            fill_datetime_field(self.driver, 'compra_DataAberturaProposta', start_date_field)
            fill_datetime_field(self.driver, 'compra_DataEncerramentoProposta', end_date_field)
            fill_datetime_field(self.driver, 'compra_dat_contratacao_lic', contract_date)

            print('Local de data inseridas')

            # local processo administrativo
            field_pa = self.driver.find_element(By.ID, 'compra_NumeroProcesso')
            field_pa.send_keys(self.info_bid['PA'])

            print('Local do Processo Adm escrito')

            # selecionar tipo do documento
            select_type_doc = self.driver.find_element(By. ID, 'compra_TipoDocumentoId')
            type_doc = Select(select_type_doc)
            type_doc.select_by_visible_text(self.register.get_type_document())

            print('Opção tipo de documento selecionada')

            # upload de arquivo
            field_upload_file = self.driver.find_element(By.ID, 'payload')
            field_upload_file.send_keys(find_file_in_directory(self.default_dir, 'Aviso'))

            # selecionar código da unidade compradora
            select_code_unity_buy = self.driver.find_element(By. ID, 'compra_CodigoUnidadeCompradora')
            code_unity_buy = Select(select_code_unity_buy)
            code_unity_buy.select_by_visible_text(self.register.get_code_unity_buy())

            print('Opção unidade compradora selecionada')

            # local objeto
            field_object = self.driver.find_element(By.ID, 'ObjetoCompra')
            field_object.send_keys(self.info_bid['Objeto'])

            print('Local do Objeto escrito')

            # chamando a função de adicionar itens
            self.add_item()

            #field_cadastrar = self.driver.find_element(By. ID, 'Salvar')
            #field_cadastrar.click()
            #print('Botão de Cadastrar clicado')

            time.sleep(10)

        except Exception as e:
            print(f'{e}: Algum erro encontrado')

    def add_item(self):
        lista_itens = extract_all_items()

        for item in lista_itens:
            botao_add_itens = self.driver.find_element(By. ID, 'add-item-compra')
            botao_add_itens.click()

            # Espera a aba de adicionar itens estar visível para começar o preenchimento dos campos
            # Utilizando o campo de descrição como exemplo de seletor a estar visível
            field_descricao = WebDriverWait(self.driver, 7).until(
                EC.visibility_of_element_located((By.ID, 'Descricao'))
            )
            field_descricao.send_keys(item['Descrição'])

            texto_desejado_julgamento = str(item['Critério de Julgamento']).lower().strip().replace('–', '-')
            select_julgamento = self.driver.find_element(By.ID, 'CriterioJulgamentoId')
            julgamento_select = Select(select_julgamento)
            normalize_select_option_item(julgamento_select, texto_desejado_julgamento)

            field_und = self.driver.find_element(By.ID, 'UnidadeMedida')
            field_und.send_keys(item['Unidade Medida'])

            select_type_item = self.driver.find_element(By.ID, 'MaterialOuServico')
            type_item_select = Select(select_type_item)
            type_item_select.select_by_visible_text(item['Material ou Serviço'])

            field_num_item = self.driver.find_element(By.ID, 'NumeroItem')
            field_num_item.send_keys(item['Número do Item'])

            field_quantidade_item = self.driver.find_element(By.ID, 'Quantidade')
            field_quantidade_item.send_keys(item['Quantidade'])

            field_valor_total = self.driver.find_element(By.ID, 'ValorTotal')
            field_valor_total.send_keys(item['Valor Total'])

            field_valor_unit = self.driver.find_element(By.ID, 'ValorUnitarioEstimado')
            field_valor_unit.send_keys(item['Valor Unitário Estimado'])

            select_incentivo = self.driver.find_element(By.ID, 'IncentivoProdutivoBasico')
            incentivo_select = Select(select_incentivo)
            incentivo_select.select_by_visible_text(item['Incentivo Produto Básico'])

            texto_desejado_beneficio = str(item['Tipo de Benefício']).lower().strip().replace('–', '-')
            select_tipo_beneficio = self.driver.find_element(By. ID, 'TipoBeneficioId')
            tipo_beneficio_select = Select(select_tipo_beneficio)
            normalize_select_option_item(tipo_beneficio_select, texto_desejado_beneficio)

            select_orcamento_sigilioso = self.driver.find_element(By.ID, 'OrcamentoSigiloso')
            orcamento_sigiloso_select = Select(select_orcamento_sigilioso)
            orcamento_sigiloso_select.select_by_visible_text(item['Orçamento Sigiloso'])

            texto_desejado_categoria = str(item['Categoria do Item']).lower().strip().replace('–', '-')
            select_categoria_item = self.driver.find_element(By.ID, 'ItemCategoriaId')
            categoria_item_select = Select(select_categoria_item)
            normalize_select_option_item(categoria_item_select, texto_desejado_categoria)

            botao_submit = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'btn-add-item-compra'))
            )

            # Rolar até o botão para garantir visibilidade
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_submit)
            botao_submit.click()

            # Espera até o elemento escolhido (Descrição) esteja invisível para repetir o ciclo
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.ID, 'Descricao'))
            )

            time.sleep(5)

    def quit_app(self):
        self.driver.quit()
        

if __name__ == '__main__':
    auto = Automation()
    auto.run_script()