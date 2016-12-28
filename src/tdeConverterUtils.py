#######################################################################################################
# Examples of usage and expected output values are documented with unit tests in test_tdeConverter.py #
#######################################################################################################

import xlrd
import csv
import dataextract as tde
from dateutil.parser import parse


class ReaderXLS:
    def __init__(self, directory,sheetName):
        self.workbook = xlrd.open_workbook(directory)
        self.worksheet = self.workbook.sheet_by_name(sheetName)
        self.currentRow = 0
        self.nrows = self.worksheet.nrows

    def __iter__(self):
        return self

    def next(self):
        if self.nrows == self.currentRow:
            raise StopIteration
        else:
            res = self.worksheet.row_values(self.currentRow)
            self.currentRow += 1
            return res

def readCSV(csvFile):
    #csvReader = csv.reader(open(csvFile,'rb'),delimiter=',',quotechar='"')
    return csv.reader(open(csvFile,'rU'), dialect=csv.excel_tab, delimiter=',')

class IntType:
    def __init__(self):
        self.tdeType = tde.Type.INTEGER

    def setType(self,row,column,element):
        return row.setInteger(column,int(float(element)))

class BoolType:
    def __init__(self):
        self.tdeType = tde.Type.BOOLEAN

    def setType(self,row,column,element):
        return row.setBoolean(column,bool(int(float(element))))

class DoubleType:
    def __init__(self):
        self.tdeType = tde.Type.DOUBLE

    def setType(self,row,column,element):
        return row.setDouble(column,float(element))

class DateType:
    def __init__(self):
        self.tdeType = tde.Type.DATE

    def setType(self,row,column,element):
        date = parse(element)
        return row.setDate(column,date.year,date.month,date.day)

class DateTimeType:
    def __init__(self):
        self.tdeType = tde.Type.DATETIME

    def setType(self,row,column,element):
        date = parse(element)
        return row.setDateTime(column,date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond)

class CharStringType:
    def __init__(self):
        self.tdeType = tde.Type.CHAR_STRING

    def setType(self,row,column,element):
        return row.setCharString(column,element)

class UnicodeStringType:
    def __init__(self):
        self.tdeType = tde.Type.UNICODE_STRING

    def setType(self,row,column,element):
        return row.setString(column,element)

# Define type maps
typesDict = {
    'Bool' :            BoolType(),
    'Int':              IntType(),
    'Double':           DoubleType(),
    'Date':             DateType(),
    'DateTime':         DateTimeType(),
    'CharString':       CharStringType(),
    'UnicodeString':    UnicodeStringType()
}


def insertRow(row,column,element,elementType):
    return typesDict[elementType].setType(row,column,element)    

# Infer type of each column in the file

def typeIdentifier(reader):
    columns = reader.next()
    numColumns = len(columns)

    typesTable = createTable(numColumns)

    for line in reader:
        columnIndex = 0
        for object in line:
            typesTable[columnIndex] = validPossibleType(typesTable[columnIndex],object)                    
            columnIndex = columnIndex + 1

    res = []
    for i in range(numColumns):
        res.append(chooseFirstValidType(typesTable[i]))

    return res

def validPossibleType(possibleColumnTypes,value):
    if not detectBool(value):
        possibleColumnTypes['Bool'] = False

    try:
        parsed2float = float(value)
        parsed2int = int(parsed2float)
        if parsed2float - parsed2int != 0:
            possibleColumnTypes['Int'] = False

        possibleColumnTypes['Date'] = False
        possibleColumnTypes['DateTime'] = False
        return possibleColumnTypes

    except:
        possibleColumnTypes['Int'] = False
        possibleColumnTypes['Double'] = False

    try:
        date = parse(value)
        if validDateTime(value):
            possibleColumnTypes['Date'] = False
        else:
            possibleColumnTypes['DateTime'] = False            
        possibleColumnTypes['Int'] = False
        possibleColumnTypes['Double'] = False

    except:
        possibleColumnTypes['Date'] = False
        possibleColumnTypes['DateTime'] = False            
        possibleColumnTypes['Int'] = False
        possibleColumnTypes['Double'] = False

    if isinstance(value, unicode):
        possibleColumnTypes['CharString'] = False

    return possibleColumnTypes

def validDateTime(value):
    for i in value:
        if i == ':':
            return True
    return False

def detectBool(s):
    if s in ['True','true','1','False','false','0','TRUE','FALSE']:
        return True
    return False

def chooseFirstValidType(typesVector):
    for t in ['Bool','Int','Double','DateTime','Date','UnicodeString','CharString']:
        if typesVector[t]:
            return t

def createTable(numColumns):
    table = []
    for i in range(numColumns):
        table.append({'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True})
    return table

