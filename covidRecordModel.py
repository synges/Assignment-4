class CovidRecordModel:
    '''A record object used to hold a record from our csv file'''

    def __init__(self, recordID, pruid, prname, prnameFR, date, numconf, numprob, numdeaths, numtotal, numtoday, ratetotal):
        '''Method that constructs all the necessary attributes and assign their values for the CovidRecord object'''
        self.recordID = recordID
        self.pruid = pruid
        self.prname = prname
        self.prnameFR = prnameFR
        self.date = date
        self.numconf = numconf
        self.numprob = numprob
        self.numdeaths = numdeaths
        self.numtotal = numtotal
        self.numtoday = numtoday
        self.ratetotal = ratetotal
