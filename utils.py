import os
import re
from datetime import datetime, timedelta
from unidecode import unidecode
import pandas as pd

from selenium.webdriver.common.by import By

from config import MONTHS


def find_file_in_directory(directory, keyword):
    """
    Função responsável por retornar o arquivo pedido no campo respectivo
    """

    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f'Diretório {directory} não encontrado.')
        return None
    
    for filename in files:
        if keyword in filename:
            return os.path.join(directory, filename)
        
    return 


def fill_datetime_field(driver, field_id, value):
    """
    Preenche um campo datetime-local utilizando JavaScript para definir o valor e disparar eventos,
    garantindo que a validação do front-end reconheça o valor.
    
    :param driver: instância do Selenium WebDriver
    :param field_id: ID do campo input datetime-local
    :param value: string no formato ISO 'YYYY-MM-DDTHH:MM'
    """
    field = driver.find_element(By.ID, field_id)
    js_script = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input'));
        arguments[0].dispatchEvent(new Event('change'));
    """
    driver.execute_script(js_script, field, value)


def convert_datetime_to_iso(lines):
    """
    Função que transforma o data capturada pelo extrato, em formato ISO. Formato esse, aceito pelo
    HTML da página
    """
    contract_date = None
    regex_data = re.compile(r'\d{2}\/\d{2}\/\d{4}')

    for line in lines:
        if regex_data.search(line):
            contract_date = line[:10] # captura os 10 primeiros caracteres que são a data de assinatura do contrato
            break

    contract_date_datetime = datetime.strptime(f'{contract_date}', '%d/%m/%Y')
    contract_date_iso = contract_date_datetime.strftime('%Y-%m-%dT13:00')

    return contract_date_iso


def calculate_useful_period(lines):
    """
    Calcula o prazo util de contratação a partir da data capturada do Aviso de Dispensa
    """

    date_regex = re.compile(r'^\d{2}.+\d{4}$')
    start_date = None

    for line in lines:
            if date_regex.search(line):
                start_date = line # captura o primeiro match do texto
                break

    num_month = None
    num_datetime = None

    # Itera sobre o dicionário de meses para pegar seu correspondente numerico - Capturando a data de início do aviso
    for month in MONTHS:
        if month in start_date: # Verifica se o mês esta na string capturada
            num_month = MONTHS[month] # Captura o valor numerico do mês
            num_datetime = f'{start_date[:2]}/{num_month}/{start_date[-4:]}' # Transforma a string escrita (10 de outubro de 2025 ) em string por extenso em dd/mm/yyyy
            break

    start_date_formated = datetime.strptime(f'{num_datetime}', '%d/%m/%Y') # Transforma a data capturada em um objeto datetime
    start_date_iso = start_date_formated.strftime('%Y-%m-%dT13:00') # Transforma o objeto datetime em formato ISO 8601

    end_date_formated = start_date_formated + timedelta(days=3) # Calcula a data final como data inicial + 3
    end_date_iso = end_date_formated.strftime('%Y-%m-%dT13:00') # Transforma a data final em formato ISO 8601

    # Faz a verificação para saber se a data final cairá num final de semana
    if start_date_formated.weekday() == 2: # Quarta
        end_date_formated = start_date_formated + timedelta(days=5)
        end_date_iso = end_date_formated.strftime('%Y-%m-%dT13:00')

    elif start_date_formated.weekday() == 3: # Quinta
        end_date_formated = start_date_formated + timedelta(days=5)
        end_date_iso = end_date_formated.strftime('%Y-%m-%dT13:00')

    elif start_date_formated.weekday() == 4: # Sexta
        end_date_formated = start_date_formated + timedelta(days=5)
        end_date_iso = end_date_formated.strftime('%Y-%m-%dT13:00')
        
    return start_date_iso, end_date_iso


def normalize_text(text):
    """
    Função que faz a normalização do texto da lei retirado do extrato. Fazendo com que as pontuações e os espaços sejam retirados
    Ex1: ART 75, CAPUT, INCISO II DA LEI 14.133/21 -> art_75_caput_inciso_ii_da_lei_1413321
    Ex2: ART 75, CAPUT, INCISO III, ALÍNEA "A" DA LEI 14.133/21 -> art_75_caput_inciso_iii_alinea_a_da_lei_1413321
    """
    text = unidecode(text.lower())
    text = re.sub(r'[\.\,\-\(\)\/\"]', '', text)  # Retirando as pontuações
    text = re.sub(r'\s+', ' ', text).strip()  # Retirando todos os espaços a mais
    text = re.sub(r'fundamentacao legal[:\s]*', '', text, flags=re.IGNORECASE)  # Retirando o termo 'fundamentacao legal'
    text = text.replace(' ', '_')
    return text


def remove_stopwords(text):
    """
    Função que remove as stopwords específicas que podem ser retiradas do extrato, como inciso, caput, lei, etc.
    A remoção é necessária para que a saída seja:
    Ex1: art_75_caput_inciso_ii_da_lei_1413321 -> art_75_ii
    Ex2: art_75_caput_inciso_iii_alinea_a_da_lei_1413321 -> art_75_iii_a

    Essa saída fará referência que as chaves referenciadas no arquivo config.py, para capturar os valores
    correspondentes e selecionar via selenium

    A ordem de chamada é normalizar_texto() -> remove_stopwords()
    """
    law_stopwords = ['da', 'de', 'lei', 'caput', 'do', 'inciso', '1413321', 'alinea', '866693']
    words = text.split('_')  # Aqui faz split por underlinetext.split()
    filtered = [word for word in words if word not in law_stopwords]
    return '_'.join(filtered)


def extract_all_items(df):

    linha = 1

    return {
        'index': df.iloc[linha]['Número do Item'],
        'descricao': df.iloc[linha]['Descrição'],
        'und': df.iloc[linha]['Unidade Medida'],
        'qtd': df.iloc[linha]['Quantidade'],
        'valor_unit': df.iloc[linha]['Valor Unitário Estimado'],
        'valor_total': df.iloc[linha]['Valor Total']
    }