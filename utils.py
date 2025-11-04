import os


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
        
    return None