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

FUNDAMENTO_LEGAL = {
    'Modalidade': {
        '8 - Dispensa de Licitação': {
            'Art. 75, Inciso I': '18 - Lei 14.133/2021, Art. 75, I',
            'Art. 75, Inciso II': '19 - Lei 14.133/2021, Art. 75, II',
            'Art. 75, Inciso III a': '20 - Lei 14.133/2021, Art. 75, III, a',
            'Art. 75, Inciso III b': '21 - Lei 14.133/2021, Art. 75, III, b',
        },

        '9 - Inexigibilidade': {
            'Art. 74, Inciso I': '6 - Lei 14.133/2021, Art. 74, I',
            'Art. 74, Inciso II': '7 - Lei 14.133/2021, Art. 74, II',
            'Art. 74, Inciso III': '8 - Lei 14.133/2021, Art. 74, III, a',
            'Art. 74, Inciso III': '9 - Lei 14.133/2021, Art. 74, III, b',
            'Art. 74, Inciso III': '10 - Lei 14.133/2021, Art. 74, III, c',
            'Art. 74, Inciso III': '11 - Lei 14.133/2021, Art. 74, III, d',
            'Art. 74, Inciso III': '12 - Lei 14.133/2021, Art. 74, III, e',
            'Art. 74, Inciso III': '13 - Lei 14.133/2021, Art. 74, III, f',
            'Art. 74, Inciso III': '14 - Lei 14.133/2021, Art. 74, III, g',
            'Art. 74, Inciso III': '15 - Lei 14.133/2021, Art. 74, III, h',
            'Art. 74, Inciso IV': '16 - Lei 14.133/2021, Art. 74, IV',
            'Art. 74, Inciso V': '17 - Lei 14.133/2021, Art. 74, V',
        },

        '12 - Credenciamento': {
            'Regulamento': '125 - Regulamento Interno de Licitações e Contratos Estatais - credenciamento'
        }
    }
}

MONTHS = {
     'Janeiro': '1',
     'Jevereiro': '2',
     'Março': '3',
     'Abril': '4',
     'Maio': '5',
     'Junho': '6',
     'Julho': '7',
     'Agosto': '8',
     'Setembro': '9',
     'Outubro': '10',
     'Novembro': '11',
     'Dezembro': '12',
}