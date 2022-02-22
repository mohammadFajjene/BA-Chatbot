import camelot
import mysql.connector
import xlrd


# read target pdf
tables = camelot.read_pdf('Dozent.pdf', pages='all')
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


# create doctor table
doctors = 'CREATE TABLE  if not exists  doctors (name VARCHAR(255), function VARCHAR(255), mobile varchar (255), email varchar (255))'

myCursor.execute(doctors)


# insert to doctors table
insertStatement = 'insert into  doctors(name, function, mobile, email) values(%s, %s, %s, %s)'



# preparing insertion values
for i in range(0, tables.n):

        tables[i].to_excel('table ' + i.__str__() + '.xls', index=False, header=None)
        book = xlrd.open_workbook("table " + i.__str__() + ".xls")
        # print(book.sheet_names())
        sheet = book.sheet_by_name(book.sheet_names()[0])
        #print(sheet.nrows)
        name = ''
        function = ''
        mobile = ''
        email = ''

        for row_num in range(sheet.nrows):
            row_value = sheet.row_values(row_num)
            name = row_value[0]
            function = row_value[1]
            mobile = row_value[2]
            email = row_value[3]

            values = [name, function, mobile, email]
            myCursor.execute(insertStatement, values)