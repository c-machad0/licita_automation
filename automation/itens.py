import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.base_manager import BaseAutomation


from utils import extract_all_items, normalize_select_option_item

class ItensManager():

    def __init__(self, driver):
       self.driver = driver


    def add_item(self):
        lista_itens = extract_all_items()

        if not lista_itens:
            print('Nenhum item encontrado.')
            return
        
        for item in lista_itens:
            botao_add_itens = self.driver.find_element(By. ID, 'add-item-compra')
            botao_add_itens.click()

            # Espera a aba de adicionar itens estar visível para começar o preenchimento dos campos
            # Utilizando o campo de descrição como exemplo de seletor a estar visível
            field_descricao = WebDriverWait(self.driver, 10).until(
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

            botao_submit = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btn-add-item-compra'))
            )

            # Rolar até o botão para garantir visibilidade
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_submit)
            botao_submit.click()

            # Espera até o elemento escolhido (Descrição) esteja invisível para repetir o ciclo
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.ID, 'Descricao'))
            )

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'add-item-compra'))
            )

            time.sleep(5)