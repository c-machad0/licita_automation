import os
from dotenv import load_dotenv

load_dotenv()

URLS = ['https://www.itajuipe.ba.gov.br/Account/Login']

LOGIN = {
    'user': os.getenv("login_user"),
    'password': os.getenv("login_pass")
}

DEFAULT_DIRECTORY = os.getenv('default_directory')