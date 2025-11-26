from automation.base_manager import BaseAutomation

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.base_manager import BaseAutomation

class UploadManager(BaseAutomation):

    def __init__(self, driver):
          self.driver = driver

          
    # LicitacaoContrato/FasesLicitacao/
    def upload_arquivos_licitacao(self):

        # Espera algum seletor estar visível para seguir o fluxo da função. Nesse caso, o seletor de Numero da Licitação
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'search_NumeroLicitacao'))
        )

        #if self.consult_licita():
        try:
                field_fases = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div/div/article/div/table/tbody/tr[2]/td[12]/a/span[@title='Fases']"))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field_fases)
                field_fases.click()
        except Exception:
                print('Botão não encontrado')
        #else:
        #    print('Licitação não encontrada.')

        field_contrato_pncp = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Pendente"))
            )
        field_contrato_pncp.click()
        # Função para registro do contrato

        field_extrato = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ButtonFase_15'))
        )
        field_extrato.click()
        # Função para upload do extrato

        field_ratificacao = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'ButtonFase_16'))
        )
        field_ratificacao.click()
        # Função para upload da ratificação

        time.sleep(5)