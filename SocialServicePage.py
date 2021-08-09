from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import yaml

class SocialServicePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.driver.get(url)
        self.xpath = None
        with open('xpath.yaml', 'r') as file:
            self.xpath = yaml.safe_load(file)['SocialServicePage']

    def read_table(self, table_xpath):
        keys = self.driver.find_elements_by_xpath(table_xpath + '/tr/th')
        values = self.driver.find_elements_by_xpath(table_xpath + '/tr/td')
        table = {key.text:value.text for key, value in zip(keys,values)}
        return table


    @property
    def title(self):
        title_xpath = self.xpath['title']
        tit = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, title_xpath))
        )
        return tit.text

    @property
    def responsable(self):
        resp_xpath = self.xpath['responsable']
        return self.read_table(resp_xpath)

    @property
    def coordinator(self):
        coor_xpath = self.xpath['coordinator']
        table = self.read_table(coor_xpath)
        if table == {}:
            table['Nombre completo'] = '-'
            table['E-mail'] = '-'
        return table

    @property
    def activities(self):
        act_xpath = self.xpath['activities']
        act = self.driver.find_elements_by_xpath(act_xpath + '/tr/td')
        act = act[1].text
        return act

    @property
    def general(self):
        obj_xpath = self.xpath['general']
        return self.read_table(obj_xpath)
        
