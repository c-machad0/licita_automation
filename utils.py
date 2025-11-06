import os

from selenium.webdriver.common.by import By


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