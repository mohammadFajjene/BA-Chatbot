from bs4 import BeautifulSoup
import requests
import time



def getInfo():
    departmentNames = []
    info = []
    infoDictAll = dict()
    htmlTxet = requests.get('https://www.eti.uni-siegen.de/dekanat/studium/pruefungsaemter/kontakt/?lang=de/data.html').text

    soup = BeautifulSoup(htmlTxet, 'lxml')
    departments = soup.findAll('h2')

    for department in departments:
        departmentNames.append(department.text)
    departmentNames.insert(0, 'Kontakt')
    # print(f'Available Departments: {departmentNames}')

    blocks = soup.findAll('div', class_='block')

    i=0
    for block_ in blocks:
        blockRows = block_.table.tbody.findAll('tr')
        info = []
        for blockRow in blockRows:
            rowItems = blockRow.findAll('td')
            for rowItem in rowItems:
                info.append(' '.join(rowItem.text.replace(':', '').split()))
        infoDict = {info[i]: info[i + 1] for i in range(0, len(info), 2)}
        infoDictAll[departmentNames[i]]=infoDict
        i=i+1
    #print(infoDictAll)
    # print(list(infoDictAll.keys())[1])
    # print(len(infoDict))
    return [infoDictAll, departmentNames]


if __name__ == '__main__':
    while True:
        #getInfo()
        print('Waiting 10 Seconds before run ...')
        time.sleep(10)
