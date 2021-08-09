from tabulate import tabulate
from ScraperSIASS import ScraperSIASS, FilterSIASS
from SocialServicePage import SocialServicePage
from time import sleep
from selenium import webdriver
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

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
        report.append([
                page.title, 
                resp['Nombre completo']+': '+resp['E-mail'],
                coor['Nombre completo']+': '+coor['E-mail'],
                page.activities,
                general['Objetivo']
        ])
    spider.quit()
    elems = []
    pdf = SimpleDocTemplate(
        'report.pdf',
        pagesize=letter
    )
    table = Table(report, colWidths=120)
    style = TableStyle([
        ('BACKGROUND', (0,0), (0,4), colors.whitesmoke),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige)
    ])
    table.setStyle(style)
    elems.append(table)
    pdf.build(elems)
    

if __name__ == '__main__':
    main()