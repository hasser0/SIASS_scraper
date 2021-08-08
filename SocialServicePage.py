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
        keys = self.driver.find_elements_by_xpath(resp_xpath + '/tr/th')
        values = self.driver.find_elements_by_xpath(resp_xpath + '/tr/td')
        resp = {key.text:value.text for key, value in zip(keys,values)}
        return resp

    @property
    def coordinator(self):
        coor_xpath = self.xpath['coordinator']
        keys = self.driver.find_elements_by_xpath(coor_xpath + '/tr/th')
        values = self.driver.find_elements_by_xpath(coor_xpath + '/tr/td')
        coor = {key.text:value.text for key, value in zip(keys,values)}
        return coor

    @property
    def activities(self):
        pass

    @property
    def objetive(self):
        pass
        
