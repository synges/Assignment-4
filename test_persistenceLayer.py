import persistenceLayer
from covidRecordModel import CovidRecordModel

test_record = CovidRecordModel(
    1, 1, "test", "testFR", "2020-12-12", 1, 1, 1, 1, 1, 1)


def test_createRecord():
    ''' test function to test the creating of a covid record and inserting it into the database'''

    createdRecodID = persistenceLayer.createRecord(test_record)

    test_record.recordID = createdRecodID

    persistenceLayer.mycursor.execute(
        "SELECT * FROM records WHERE recordID = %s", (test_record.recordID, ))

    result = persistenceLayer.mycursor.fetchone()

    # Ahmed Aziz!!!!!

    assert result["pruid"] == test_record.pruid
    assert result["prname"] == test_record.prname
    assert result["prnameFR"] == test_record.prnameFR
    assert result["date"] == test_record.date
    assert result["numconf"] == test_record.numconf
    assert result["numprob"] == test_record.numprob
    assert result["numdeaths"] == test_record.numdeaths
    assert result["numtotal"] == test_record.numtotal
    assert result["numtoday"] == test_record.numtoday
    assert result["ratetotal"] == test_record.ratetotal
    # # Ahmed Aziz!!!!!


def test_updateRecord():
    ''' test function to test updating of a covid record in the database'''

    newName = "New name"

    test_record.prname = newName

    persistenceLayer.updateRecord(test_record)

    persistenceLayer.mycursor.execute(
        "SELECT * FROM records WHERE recordID = %s", (test_record.recordID, ))

    result = persistenceLayer.mycursor.fetchone()

    assert result["prname"] == newName


def test_deleteRecord():
    ''' test function to test deleting of a covid record in the database'''

    persistenceLayer.deleteRecord(test_record.recordID)

    persistenceLayer.mycursor.execute(
        "SELECT * FROM records WHERE recordID = %s", (test_record.recordID, ))

    result = persistenceLayer.mycursor.fetchone()

    assert result == None
