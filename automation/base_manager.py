from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


from config import DEFAULT_DIRECTORY, DOWNLOAD_DIRECTORY
from reader import Register


class BaseAutomation:
    def __init__(self):
        self.default_dir = DEFAULT_DIRECTORY
        self.options = Options()

        prefs = {
            "download.default_directory": DOWNLOAD_DIRECTORY,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }

        self.options.add_experimental_option("prefs", prefs)

        self.service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.maximize_window() # Fazer com que as janelas sempre sejam maximizadas

        self.register = Register()
        # select_field() popula os atributos self.modality_found_dict, self.instrumento e self.modo_disputa.
        # Os mtodos getter acessam esses atributos.
        self.register.read_doc()
        self.register.select_field()
        self.register.read_extract_to_law()
        self.info_bid = self.register.write_field()


    def quit_app(self):
        self.driver.quit()
    