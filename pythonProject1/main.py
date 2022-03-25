from bs4 import BeautifulSoup
import requests
import time

# declare lists
departmentNames = []
info = []
infoDictAll = dict()

def getInfo():

    # get website source code
    htmlTxet = requests.get(
        'https://www.eti.uni-siegen.de/dekanat/studium/pruefungsaemter/kontakt/?lang=de/data.html').text

    # parse source code
    soup = BeautifulSoup(htmlTxet, 'lxml')

    # scraping departments
    departments = soup.findAll('h2')

    # building departments list
    for department in departments:
        departmentNames.append(department.text)
    departmentNames.insert(0, 'Kontakt')

    blocks = soup.findAll('div', class_='block')

    i = 0

    # scraping departments attributes
    for block_ in blocks:
        blockRows = block_.table.tbody.findAll('tr')
        info = []
        for blockRow in blockRows:
            rowItems = blockRow.findAll('td')
            for rowItem in rowItems:
                info.append(' '.join(rowItem.text.replace(':', '').split()))
        infoDict = {info[i]: info[i + 1] for i in range(0, len(info), 2)}
        infoDictAll[departmentNames[i]] = infoDict
        i = i + 1
    print(infoDictAll)

    return [infoDictAll, departmentNames]


if __name__ == '__main__':
    while True:
        getInfo()
        print('Waiting 10 Seconds before run ...')

        # timer to rerun script
        time.sleep(10)
