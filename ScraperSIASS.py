from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from tabulate import tabulate
import selenium
import yaml
from SocialServicePage import SocialServicePage

SIASS_MAIN = 'https://www.siass.unam.mx/'


class FilterSIASS:
    ESTADO = 'estado_id'
    MUNICIPIO = 'municipio_id'
    INSTITUTION = 'sector'
    EJE = 'eje_tematico_id'
    APOYO = 'apoyo'
    UBICACION = 'ubicacion'
    ASISTENCIA = 'asistencia'
    HORARIO = 'horario'


class ScraperSIASS:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.xpath = None
        with open('xpath.yaml', 'r') as file:
            self.xpath = yaml.safe_load(file)['ScraperSIASS']

    def login(self, account, faculty, career, system='dgae'):
        accept_xpath = self.xpath['login']['accept_btn']
        driver = self.driver
        driver.get(SIASS_MAIN)
        accept_btn = WebDriverWait(driver,10).until(
            ec.element_to_be_clickable((By.XPATH, accept_xpath))
        )
        accept_btn.click()
        #insert account number
        account_number = driver.find_element_by_name('numero_cuenta')
        account_number.send_keys(account)
        #select system
        sistema = Select(driver.find_element_by_id('combo_sistem_pertenece'))
        sistema.select_by_value(system)
        #select faculty
        facultad = Select(driver.find_element_by_id('combo_facultades'))
        facultad.select_by_value(faculty)
        #select career
        carrera = Select(driver.find_element_by_id('combo_carreras'))
        carrera.select_by_value(career)
        #submit all
        submit = driver.find_element_by_id('submit-forma')
        submit.click()

    def advance_search(self, advance_options):
        driver = self.driver
        search_xpath = self.xpath['advance_search']['search_btn']
        filter_xpath = self.xpath['advance_search']['filter_btn']
        search = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, search_xpath))
        )
        search.click()
        #Filter
        for field in advance_options:
            option = Select(WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.NAME, field))
            ))
            option.select_by_value(advance_options[field])
        filter = driver.find_element_by_xpath(filter_xpath)
        filter.click()

    def get_ss_links(self):
        driver = self.driver
        ss_xpath = self.xpath['load_ss_options']['load']
        options = driver.find_elements_by_xpath(ss_xpath)
        links = [option.get_attribute('href') for option in options]
        return links

    def change_page(self):
        driver = self.driver
        change_page_xpath = self.xpath['change_page']['change_page_btn']
        try:
            change_page_btn = WebDriverWait(driver, 3).until(
                ec.element_to_be_clickable((By.XPATH, change_page_xpath))
            )
            change_page_btn.click()
            return False
        except TimeoutException as e:
            return True

    def quit(self):
        self.driver.quit()
