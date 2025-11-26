from pypdf import PdfReader
from unidecode import unidecode


from reader.base_reader import BaseReader
from utils import find_file_in_directory, convert_datetime_to_iso, normalize_text, remove_stopwords, calculate_useful_period


class PDFProcessor(BaseReader):

    def __init__(self, base_reader: BaseReader):
        """
        Recebe base_reader como parâmetro para compartilhar estado.
        """

        self.base_reader = base_reader
        self.directory = base_reader.directory
        self.modalities = base_reader.modalities
        self.legal_basis = base_reader.legal_basis


    def read_pdf_lines(self, file_keyword):
        filepath = find_file_in_directory(self.directory, file_keyword)
        if not filepath:
            raise FileNotFoundError(f"Arquivo com keyword '{file_keyword}' não encontrado.")
        reader = PdfReader(filepath)
        page = reader.pages[0]
        text = page.extract_text()
        lines = text.split('\n')
        return lines
    

    def read_doc(self):
        """
        Função que extrai os dados necessários do texto. [modalidade, numero da modalidade,
        numero do processo administrativo e objeto]
        """

        """
        Extrai dados do PDF e ATUALIZA base_reader.
        """

        lines = self.read_pdf_lines('Contrato'.upper())

        # Encontrado a modalidade e seu numero através do texto lido
        for index, line in enumerate(lines):
            for modalidade in self.modalities:
                if modalidade in line:
                    self.base_reader.read_modality = modalidade # Armazenando a modalidade em read_modality
                    self.base_reader.read_num_modality = lines[index][-9:] # Armazenando o numero da modalidade em read_num_modality
                    break
        
        # Encontrar numero do processo adminstrativo
        for line in lines:
            if 'Processo Administrativo'.upper() in line:
                # PROCESSO ADMMINISTRATIVO N° 
                self.base_reader.read_admprocess = line[-9:]
                break
        
        result_lines = []
        found = False

        # Encontrar objeto
        for line in lines:
            if 'Objeto'.upper() in line.upper():
                found = True
                continue
            if found:
                if line.strip() == '':
                    break
                result_lines.append(line)
        
        self.base_reader.read_object = ''.join(result_lines)


    def read_extract_to_time(self):
        lines = self.read_pdf_lines('Extrato')
        converted_date = convert_datetime_to_iso(lines)
        return converted_date
    

    def read_extract_to_law(self):
        """
        Extrai fundamentação legal (depende de select_field).
        """

        lines = self.read_pdf_lines('Extrato')

        fund_legal_capturada = None

        for line in lines:
            if 'Fundamentação Legal'.upper() in line:
                fund_legal_capturada = line
                break

        text_normalized = normalize_text(fund_legal_capturada)
        clean_text = remove_stopwords(text_normalized)

        modalidade_final = None
        for key_mod in self.base_reader.legal_basis['Modalidade']:
            if unidecode(self.base_reader.modality_found_final.lower()) in unidecode(key_mod.lower()):
                modalidade_final = key_mod
                break

        if modalidade_final:
            artigos_dict = self.legal_basis['Modalidade'][modalidade_final]
            if clean_text in artigos_dict:
                self.base_reader.amparo_legal = artigos_dict[clean_text]
            else:
                return None
        else:
            return None
        

    def read_notice(self):
        lines = self.read_pdf_lines('Aviso')
        start_date, end_date = calculate_useful_period(lines)
        return start_date, end_date 