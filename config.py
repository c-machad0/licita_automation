import os
from dotenv import load_dotenv

load_dotenv()

URLS = ['https://www.itajuipe.ba.gov.br/Account/Login']

LOGIN = {
    'user': os.getenv("login_user"),
    'password': os.getenv("login_pass")
}

DEFAULT_DIRECTORY = os.getenv('default_directory')

INSERTION_BID = {
    'Modalidades':{
        'Pregão Eletrônico': '6 - Pregão - Eletrônico',
        'Pregão Presencial': '7 - Pregão - Presencial',
        'Dispensa': '8 - Dispensa de Licitação',
        'Inex': '9 - Inexigibilidade',
        'Credenciamento': '12 - Credenciamento'
    },
    'Instrumento': {
        'Edital': '1 - Edital',
        'Aviso': '2 - Aviso de Contratação Direta',
        'Ato': '3 - Ato que autoriza a Contratação Direta',
        'Edital CP': '4 - Edital de Chamamento Público'
    },
    'Modo de Disputa': {
        'Aberto': '1 - Aberto',
        'Disputa': '4 - Dispensa Com Disputa',
        'Não': '5 - Não se aplica'
    }
}
