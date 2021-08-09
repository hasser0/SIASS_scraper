from tabulate import tabulate
from ScraperSIASS import ScraperSIASS, FilterSIASS
from SocialServicePage import SocialServicePage
from time import sleep
from selenium import webdriver

def main():    
    driver = webdriver.Chrome('./chromedriver')
    spider = ScraperSIASS(driver)
    spider.login(account='316281841', faculty='38', career='21')
    options = {
        FilterSIASS.EJE: '2',
        FilterSIASS.UBICACION: '9'
    }
    spider.advance_search(options)
    links = []
    while True:
        links += spider.get_ss_links()
        if spider.change_page():
            break
    report = [['Programa', 'Responsable', 'Coordinador', 'Actividades', 'Objetivo']]
    for link in links:
        sleep(1)
        page = SocialServicePage(driver, link)
        resp = page.responsable
        coor = page.coordinator
        general = page.general
        print('Programa: ' + page.title)
        print('Responsable: '+resp['Nombre completo']+'  =>  '+resp['E-mail'])
        print('Coordinador: '+coor['Nombre completo']+'  =>  '+coor['E-mail'])
        print('Actividades: '+page.activities)
        print('Objetivo: '+general['Objetivo'])
        print('*'*50)
        print('*'*50)
    spider.quit()
    


if __name__ == '__main__':
    main()