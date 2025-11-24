import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from automation.base_manager import BaseAutomation

class NavigationManager(BaseAutomation):
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