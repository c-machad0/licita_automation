from pypdf import PdfReader
from pprint import pprint

reader = PdfReader('03. CONTRATO GASES MEDICINAIS - ITAOX.pdf')
page = reader.pages[0]
text = page.extract_text()

# Dividir o texto em linhas
linhas = text.split('\n')

# Mostrar todas as linhas para análise (opcional)
#for i, linha in enumerate(linhas):
#    print(f"Linha {i}: {linha}")

num_modalidade = linhas[10][-9:]
#print(num_modalidade)
num_processo = linhas[11][-9:]
#print(num_processo)
objeto = linhas[36] + linhas[37] + linhas[38]
#print(objeto)

info_bid = {
    'Número da Compra': num_modalidade,
    'Ano da Compra': 2025,
    'Execução': 'Prefeitura Municipal de Itajuípe',
    'Certame': 'Prefeitura Municipal de Itajuípe',
    'PA': num_processo,
    'Objeto': objeto 
}

#pprint(info_bid)
"""
Captação de n° de dispensa e processo adm: por meio dos 8 primeiros caracteres, fazendo de ordem inversa
N° da modalidade estará na linha 10
N° do PA estará na linha 11
N° do objeto da linha 36 a 38
"""