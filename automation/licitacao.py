import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from automation.base_manager import BaseAutomation
from utils import find_file_in_directory, fill_datetime_field
from reader.data_extractor import DataExtractor

class LicitaManager(BaseAutomation):

    def __init__(self, driver, info_bid, data_extractor, pdf_processor):
        self.driver = driver
        self.info_bid = info_bid
        self.data_extractor = data_extractor
        self.pdf_processor = pdf_processor


    def consult_licita(self):
        field_numero_licita = self.driver.find_element(By.ID, 'search_NumeroLicitacao')
        field_numero_licita.send_keys(self.info_bid['Número da Compra'])

        field_numero_processo = self.driver.find_element(By.ID, 'search_NumeroProcesso')
        field_numero_processo.send_keys(self.info_bid['PA'])

        # Busca por todas as células (td) que contenham esse número de licitação
        page_elements_licita = self.driver.find_elements(By.XPATH, f"//td[contains(text(), '{self.info_bid['Número da Compra']}')]")

        # Se encontrar 1 ou mais elementos, retorna que existe
        return len(page_elements_licita) > 0
    

    # /sai/ConfiguracaoPncp/InserirCompra
    def inserir_licitacao(self):

        try:
            # modalidade
            select_modalidade = self.driver.find_element(By.ID, 'compra_ModalidadeId')
            modalidade_select = Select(select_modalidade)
            modalidade_select.select_by_visible_text(self.data_extractor.get_modality())

            print('Opção de modalidade selecionada')

            time.sleep(1)

            # instrumento
            select_instrumento = self.driver.find_element(By.ID, 'compra_TipoInstrumentoConvocatorioId')
            instrumento_select = Select(select_instrumento)
            instrumento_select.select_by_visible_text(self.data_extractor.get_instrumento())

            print('Opção de instrumento selecionada')

            time.sleep(1)

            select_amparo_legal = self.driver.find_element(By. ID, 'compra_AmparoLegalId')
            amparo_legal_select = Select(select_amparo_legal)
            amparo_legal_select.select_by_visible_text(self.data_extractor.get_amparo_legal())
            
            print('Opção de amparo legal selecionada')

            time.sleep(1)

            # modo de disputa
            select_modo = self.driver.find_element(By.ID, 'compra_ModoDisputaId')
            modo_select = Select(select_modo)
            modo_select.select_by_visible_text(self.data_extractor.get_modo_disputa())

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
            start_date_field, _ = self.pdf_processor.read_notice()
            _, end_date_field = self.pdf_processor.read_notice()
            contract_date = self.pdf_processor.read_extract_to_time()

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
            type_doc.select_by_visible_text(self.data_extractor.get_type_document())

            print('Opção tipo de documento selecionada')

            # upload de arquivo
            field_upload_file = self.driver.find_element(By.ID, 'payload')
            field_upload_file.send_keys(find_file_in_directory(self.default_dir, 'Aviso'))

            # selecionar código da unidade compradora
            select_code_unity_buy = self.driver.find_element(By. ID, 'compra_CodigoUnidadeCompradora')
            code_unity_buy = Select(select_code_unity_buy)
            code_unity_buy.select_by_visible_text(self.data_extractor.get_code_unity_buy())

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