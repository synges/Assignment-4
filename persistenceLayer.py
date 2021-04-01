import csv
import os
import mysql.connector
from covidRecordModel import CovidRecordModel

db = mysql.connector.connect(
    host="localhost",
    user="Ahmed",
    passwd="5232391Aa!",
    auth_plugin='mysql_native_password',
    database="covid_records"
)
'''database connection object'''

mycursor = db.cursor(dictionary=True)
'''database cursor'''


def fetchRecords():
    '''Fuction to fetch records from the database and store them in array to be displayed'''
    # Author: Ahmed Aziz

    records = []
    '''Array to store the record objects created'''

    mycursor.execute("SELECT * FROM records")

    # Author: Ahmed Aziz
    for row in mycursor:
        '''For loop to itreate over the data_set object that store all the rows parsed from the csv file'''

        covid_record = CovidRecordModel(row['recordID'], row['pruid'], row['prname'], row['prnameFR'], row['date'], row['numconf'],
                                        row['numprob'], row['numdeaths'], row['numtotal'], row['numtoday'], row['ratetotal'])
        '''Creating a record object and storing the data of that row in it'''

        records.append(covid_record)
        '''Storing the record object created to the array'''

    return records


def createRecord(newRecord):
    '''Fuction to create a record and store insert it in the database'''
    mycursor.execute("INSERT INTO records (pruid, prname, prnameFR, date, numconf, numprob, numdeaths, numtotal, numtoday, ratetotal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (newRecord.pruid, newRecord.prname, newRecord.prnameFR, newRecord.date, newRecord.numconf,
                                                                                                                                                                                newRecord.numprob, newRecord.numdeaths, newRecord.numtotal, newRecord.numtoday, newRecord.ratetotal))
    db.commit()
    return mycursor.lastrowid
    # Author: Ahmed Aziz


def updateRecord(updatedRecord):
    '''Fuction to update a record in the database'''
    mycursor.execute("UPDATE records SET pruid = %s, prname = %s, prnameFR = %s, date = %s, numconf = %s, numprob = %s, numdeaths = %s, numtotal = %s, numtoday = %s, ratetotal = %s WHERE recordID = %s", (updatedRecord.pruid, updatedRecord.prname, updatedRecord.prnameFR, updatedRecord.date, updatedRecord.numconf,
                                                                                                                                                                                                            updatedRecord.numprob, updatedRecord.numdeaths, updatedRecord.numtotal, updatedRecord.numtoday, updatedRecord.ratetotal, updatedRecord.recordID))
    db.commit()
    # Author: Ahmed Aziz


def deleteRecord(id):
    '''Fuction to delete a record in the database'''
    mycursor.execute(
        "DELETE FROM records WHERE recordID = %s", (id,))
    db.commit()
    # Author: Ahmed Aziz


def writeToFile(recordsWrite):
    '''function to write the contents of the database to a csv file'''
    try:
        '''this try catch removes the old file to replace it with a new one(instead of appending to it) if the file dosen't exist yet then just print file not found'''
        os.remove('newCovidCsv.csv')
    except FileNotFoundError:
        print("File Not found")
    # Author: Ahmed Aziz

    with open('newCovidCsv.csv', 'w', newline='') as f:
        '''Opens/creates the file in write mode'''
        thewriter = csv.writer(f)
        '''writer object used with file f to write csv'''

        thewriter.writerow(['pruid', 'prname', 'prnameFR', 'date', 'numconf',
                            'numprob', 'numdeaths', 'numtotal', 'numtoday', 'ratetotal'])
        '''write the first row of the file which is the column names'''

        for record in recordsWrite:
            thewriter.writerow([record.pruid, record.prname, record.prnameFR, record.date, record.numconf,
                                record.numprob, record.numdeaths, record.numtotal, record.numtoday, record.ratetotal])
        '''for loop that loops threw the records writing each one to a row'''
