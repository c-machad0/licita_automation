from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


from config import DEFAULT_DIRECTORY, DOWNLOAD_DIRECTORY


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


    def quit_app(self):
        self.driver.quit()
    