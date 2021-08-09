from tabulate import tabulate
from ScraperSIASS import ScraperSIASS, FilterSIASS
from SocialServicePage import SocialServicePage
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
    with open('report.txt', 'wt') as file:
        for link in links:
            page = SocialServicePage(driver, link)
            resp = page.responsable
            coor = page.coordinator
            general = page.general
            file.write('Programa: ' + page.title+ '\n')
            file.write('Responsable: '+resp['Nombre completo']+'  =>  '+resp['E-mail']+'\n')
            file.write('Coordinador: '+coor['Nombre completo']+'  =>  '+coor['E-mail']+'\n')
            file.write('Actividades: '+page.activities+'\n')
            file.write('Disponibilidad: '+page.availability+'\n')
            file.write('Objetivo: '+general['Objetivo']+'\n\n')
    spider.quit()


if __name__ == '__main__':
    main()