from config import DEFAULT_DIRECTORY, MODALITIES, MONTHS, MODALITY_RELATIONS, LEGAL_BASIS

class BaseReader:
    def __init__(self):
        self.directory = DEFAULT_DIRECTORY
        self.modalities = MODALITIES
        self.month = MONTHS
        self.modality_relations = MODALITY_RELATIONS
        self.legal_basis = LEGAL_BASIS

        self.modality_found = None
        self.modality_found_final = None
        self.instrumento = None
        self.modo_disputa = None
        self.amparo_legal = None
        self.read_modality = None
        self.read_num_modality = None
        self.read_admprocess = None
        self.read_object = None
        self.type_doc = None
        self.code_unity_buy = None
        