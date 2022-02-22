import mysql.connector
import main


# database connector
myDB = mysql.connector.connect(
  host="localhost",
  user="root",
  password="000000"
)

# define cursor to execute statements
myCursor = myDB.cursor()

# create database
myCursor.execute("CREATE DATABASE if not exists mydatabase CHARACTER SET utf8 COLLATE utf8_general_ci")
myCursor.execute("use mydatabase")

# create departments table
departmentsTable = 'CREATE TABLE  if not exists  departmentsTable (name VARCHAR(255),' \
                                                                  'contact VARCHAR(255),' \
                                                                  'phone varchar (255), ' \
                                                                  'fax varchar (255), ' \
                                                                  'email varchar (255), ' \
                                                                  'address varchar (255), ' \
                                                                  'openingHours varchar (255),' \
                                                                  'unique (name))'

myCursor.execute(departmentsTable)

# preparing values
for i in range(0, len(main.getInfo()[1])-1):

    name = main.getInfo()[1][i+1]
    contact = main.getInfo()[0][main.getInfo()[1][i+1]]['Kontakt'].__str__()
    phone = main.getInfo()[0][main.getInfo()[1][i+1]]['Telefon'].__str__()
    fax = main.getInfo()[0][main.getInfo()[1][i+1]]['Fax'].__str__()
    email = main.getInfo()[0][main.getInfo()[1][i+1]]['Email'].__str__()
    address = main.getInfo()[0][main.getInfo()[1][0]]['Adresse'].__str__()
    openingHours = main.getInfo()[0][main.getInfo()[1][0]]['Öffnungszeiten'].__str__()

    insertValues = [name, contact, phone, fax, email, address, openingHours, contact, phone, fax, email, address, openingHours]

    insertStatement = 'insert into  departmentsTable(name, contact, phone, fax, email, address, openingHours)  ' \
                                             'values(%s, %s, %s, %s, %s, %s, %s)' \
                                             'ON DUPLICATE KEY UPDATE  ' \
                                             'contact = %s, ' \
                                             'phone = %s, ' \
                                             'fax= %s,' \
                                             'email= %s,' \
                                             'address= %s,' \
                                             'openingHours= %s'
    myCursor.execute(insertStatement, insertValues)





