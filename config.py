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
            'art_75_i': '18 - Lei 14.133/2021, Art. 75, I',
            'art_75_ii': '19 - Lei 14.133/2021, Art. 75, II',
            'art_75_iii_a': '20 - Lei 14.133/2021, Art. 75, III, a',
            'art_75_iii_b': '21 - Lei 14.133/2021, Art. 75, III, b',
        },

        '9 - Inexigibilidade': {
            'art_74_i': '6 - Lei 14.133/2021, Art. 74, I',
            'art_74_ii': '7 - Lei 14.133/2021, Art. 74, II',
            'art_74_iii_a': '8 - Lei 14.133/2021, Art. 74, III, a',
            'art_74_iii_b': '9 - Lei 14.133/2021, Art. 74, III, b',
            'art_74_iii_c': '10 - Lei 14.133/2021, Art. 74, III, c',
            'art_74_iii_d': '11 - Lei 14.133/2021, Art. 74, III, d',
            'art_74_iii_e': '12 - Lei 14.133/2021, Art. 74, III, e',
            'art_74_iii_f': '13 - Lei 14.133/2021, Art. 74, III, f',
            'art_74_iii_g': '14 - Lei 14.133/2021, Art. 74, III, g',
            'art_74_iii_h': '15 - Lei 14.133/2021, Art. 74, III, h',
            'art_74_iv': '16 - Lei 14.133/2021, Art. 74, IV',
            'art_74_v': '17 - Lei 14.133/2021, Art. 74, V',
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