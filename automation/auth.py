import time

from selenium.webdriver.common.by import By

from automation.base_manager import BaseAutomation
from config import URLS, LOGIN

class AutenticationManager(BaseAutomation):

    def access_url(self):
        self.driver.get(URLS[0])
    
    # /Account/Login
    def login(self):
        text_field = self.driver.find_elements(By.CSS_SELECTOR, 'main.login .box form .input input')

        user_input = text_field[0]
        password_input = text_field[1]

        user_input.send_keys(LOGIN['user'])
        password_input.send_keys(LOGIN['password'])

        if user_input and password_input:
            button_login = self.driver.find_element(By.CSS_SELECTOR, 'main.login .box form button, main.login .box form input[type="submit"]')
            button_login.click()

        time.sleep(5)