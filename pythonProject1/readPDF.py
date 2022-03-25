import camelot
import mysql.connector
import pandas as pd
import ctypes
import tkinter
import xlrd
import fitz
from ctypes.util import find_library

# database connector
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="000000"
)

myCursor = myDB.cursor()

myCursor.execute("use mydatabase")

# create subject table
subject = 'CREATE TABLE  if not exists  subject (name VARCHAR(255), level VARCHAR(255), lecturer varchar (255), language varchar (255), hours varchar (1000),points varchar (255))'

myCursor.execute(subject)


# insert to subject table
insertStatement = 'insert into  subject(name, level, lecturer, language, hours, points)  values(%s, %s, %s, %s, %s, %s)'




# read target pdf
tables = camelot.read_pdf('https://www.eti.uni-siegen.de/dekanat/studium/pruefungsaemter/dokumente/modulhandbuecher/modulhandbuch_bama_inf.pdf',
                          pages='7-')
# print (tables[0].parsing_report)
print("tables in pdf is : " + tables.n.__str__())


# preparing insertion values
for i in range(0, tables.n):

        tables[i].to_excel('table ' + i.__str__() + '.xls', index=False, header=None)
        book = xlrd.open_workbook("table " + i.__str__() + ".xls")
        # print(book.sheet_names())
        sheet = book.sheet_by_name(book.sheet_names()[0])
        name = ''
        lvl = ''
        lecturer = ''
        lang = ''
        hours = ''
        points = ''
        for row_num in range(sheet.nrows):
            row_value = sheet.row_values(row_num)

            if row_value[0].startswith('Modulbezeichnung'):
                name = row_value[1]
                # print(name.__str__())

            if row_value[0].startswith('Modulniveau') or row_value[0].startswith('ggf. Modulniveau'):
                lvl = row_value[1]
                # print(lvl.__str__())

            if (row_value[0].startswith('Modulverantwortliche') or row_value[0].startswith('Lehrende')) and lecturer == '':
                lecturer = row_value[1]
                # print(lecturer.__str__())

            if row_value[0].startswith('Sprache') or row_value[0].startswith('Lehrsprache'):
                lang = row_value[1]
                # print(lang.__str__())

            if row_value[0].startswith('Arbeitsaufwand') or row_value[0].startswith('Präsenzstudium in'):
                hours = row_value[1]
                # print(hours.__str__())

            if row_value[0].startswith('Kreditpunkte') or row_value[0].startswith('Leistungspunkte'):
                points = row_value[1]
                # print(points.__str__())

        values = [name, lvl, lecturer, lang, hours, points]
        # print(values.__str__())

        # distinguish between single page table and multi-pages expanding table
        if '' not in values:
             myCursor.execute(insertStatement, values)
