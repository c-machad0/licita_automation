import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

URLS = ['https://www.itajuipe.ba.gov.br/Account/Login']

LOGIN = {
    'user': os.getenv("login_user"),
    'password': os.getenv("login_pass")
}

DEFAULT_DIRECTORY = os.getenv('default_directory')

MODALITIES = ['DISPENSA DE LICITAÇÃO', 'INEXIGIBILIDADE', 'PREGÃO ELETRÔNICO', 'PREGÃO PRESENCIAL', 'CREDENCIAMENTO']

RELACIONAMENTOS = {
    'Modalidade': {
        '8 - Dispensa de Licitação': {
            'Instrumento': ['2 - Aviso de Contratação Direta'],
            'Modo de Disputa': ['4 - Dispensa Com Disputa'],
            'Tipo de Documento': ['1 - Aviso de Contratação Direta'],
            'Código': ['2612 - Prefeitura Municipal de Itajuípe']
            
        },
        '6 - Pregão Eletrônico': {
            'Instrumento': ['1 - Edital'],
            'Modo de Disputa': ['1 - Aberto'],
            'Tipo de Documento': ['2 - Edital'],
            'Código': ['2612 - Prefeitura Municipal de Itajuípe']
            
        },
        '7 - Pregão Presencial': {
            'Instrumento': ['1 - Edital'],
            'Modo de Disputa': ['1 - Aberto'],
            'Tipo de Documento': ['2 - Edital'],
            'Código': ['2612 - Prefeitura Municipal de Itajuípe']
            
        },
        '9 - Inexigibilidade': {
            'Instrumento': ['3 - Ato que autoriza a Contratação'],
            'Modo de Disputa': ['5 - Não se aplica'],
            'Código': ['2612 - Prefeitura Municipal de Itajuípe']
        },

        '12 - Credenciamento': {
            'Instrumento': ['4 - Edital de Chamamento Público'],
            'Modo de Disputa': ['5 - Não se aplica'],
            'Tipo de Documento': ['2 - Edital']
        }
    }
}