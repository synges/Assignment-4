import mysql.connector
import csv
'''This file is used to setup the database and populate it with records from the provided csv'''

db = mysql.connector.connect(
    host="localhost",
    user="Ahmed",
    passwd="5232391Aa!",
    auth_plugin='mysql_native_password'
)
'''creating a connection to MySQL'''

mycursor = db.cursor()

mycursor.execute("DROP DATABASE IF EXISTS covid_records")
mycursor.execute("CREATE DATABASE covid_records")
'''creating a database'''

# Author: Ahmed Aziz

db = mysql.connector.connect(
    host="localhost",
    user="Ahmed",
    passwd="5232391Aa!",
    auth_plugin='mysql_native_password',
    database="covid_records"
)

mycursor = db.cursor()

mycursor.execute(
    "CREATE TABLE records (recordID int PRIMARY KEY AUTO_INCREMENT, pruid int , prname VARCHAR(50),  prnameFR VARCHAR(50), date VARCHAR(20), numconf int , numprob int , numdeaths int , numtotal int , numtoday int , ratetotal float)")
'''creating a table to hold the records'''

fileName = 'covid19-download.csv'
'''file name for the dataset'''
# Author: Ahmed Aziz

try:
    '''Try block to handle exception if the file can't be found'''

    with open(fileName) as data_file:
        '''Opens and reads the contents of the file'''

        data_set = csv.DictReader(data_file)
        '''An API that parse the contents of the csv into a Python Dictoniry object, with the keys as the first row of the csv file'''

        # Author: Ahmed Aziz
        for row in data_set:
            '''For loop to itreate over the data_set object that store all the rows parsed from the csv file'''

            mycursor.execute("INSERT INTO records (pruid, prname, prnameFR, date, numconf, numprob, numdeaths, numtotal, numtoday, ratetotal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row['pruid'], row['prname'], row['prnameFR'], row['date'], row['numconf'],
                                                                                                                                                                                        row['numprob'], row['numdeaths'] if row['numdeaths'] != '' else None, row['numtotal'], row['numtoday'], row['ratetotal'] if row['ratetotal'] != '' else None))
            '''the cursor inserts each row in the database replacing empty values with null'''


except FileNotFoundError:
    '''Catching the exception if the file is not found and print a error message to the console'''
    print("The csv file was not found in the same directory")

db.commit()
'''commiting changes to the database'''
