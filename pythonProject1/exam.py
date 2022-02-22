import camelot
import mysql.connector
import pandas as pd
import ctypes
import tkinter
import xlrd
import fitz
from _cffi_backend import typeof
from bs4 import BeautifulSoup
import requests
import time
import re



# read target pdf
tables = camelot.read_pdf('https://www.eti.uni-siegen.de/dekanat/studium/pruefungsaemter/dokumente/aushaenge/klausurtermine_ws_21_22.pdf',
                          pages='1-5')
# print (tables[0].parsing_report)
print("tables in pdf is : " + tables.n.__str__())

# database connector
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="000000"
)

myCursor = myDB.cursor()

myCursor.execute("use mydatabase")

# create exam table
exam = 'CREATE TABLE  if not exists  exam (name VARCHAR(255), date VARCHAR(255), day varchar (255), time varchar (255), tester varchar (255), room varchar (255))'

myCursor.execute(exam)

# insert into exam table
insertStatement = 'insert into  exam(name, date, day, time, tester,room)  values(%s, %s, %s, %s, %s,%s)'


# preparing values
for i in range(0, tables.n):

        tables[i].to_excel('table ' + i.__str__() + '.xls', index=False, header=None)
        book = xlrd.open_workbook("table " + i.__str__() + ".xls")

        sheet = book.sheet_by_name(book.sheet_names()[0])
        name = ''
        date = ''
        day = ''
        time = ''
        tester = ''
        room = ''

        for row_num in range(sheet.nrows):
            row_value = sheet.row_values(row_num)
            if 'Klausur'  in row_value:
                print(row_value.__str__())
                name_idx = row_value.index('Klausur')
                print('name index is : ', name_idx)
                date_idx = row_value.index('Datum')
                day_idx = row_value.index('Prüfungstag')
                time_idx = row_value.index('Uhrzeit Prüfung')
                tester_idx = row_value.index('Prüfer')
                room_idx = row_value.index('Raum')

                for sub_row in range(row_num+1, sheet.nrows):
                    row_val = sheet.row_values(sub_row)
                    name = row_val[name_idx]
                    date = row_val[date_idx]
                    day = row_val[day_idx]
                    time = row_val[time_idx]
                    tester = row_val[tester_idx]
                    room = row_val[room_idx]
                    values = [name, date, day, time, tester,room]
                    myCursor.execute(insertStatement, values)
