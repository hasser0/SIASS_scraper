from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from urllib import request

MAC_TEMARIOS = 'https://mac.acatlan.unam.mx/escolares/temarios/1644/'
def main():
    driver = webdriver.Chrome('./chromedriver')
    driver.get(MAC_TEMARIOS)
    semesters = WebDriverWait(driver, 5).until(
        ec.presence_of_all_elements_located((By.XPATH, '//a[@class="semestreActivo semestre"]'))
    )
    for sem in semesters:
        sem.click()
        sleep(2)
        classes = WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.XPATH, '//li[@class="materiasLI"]/a'))
        )
        for c in classes:
            url = c.get_attribute('href')
            r = request.urlopen(url)
            with open(c.text+".pdf",'wb') as f:
                f.write(r.read())
    driver.close()

if __name__ == '__main__':
    main()