import multiprocessing as mp
import sys
import csv

import dataextract as tde
import os
import datetime
from functools import partial

def insertRow(row,column,element,elementType):
    if elementType is 'Int':
        return row.setInteger(column,int(float(element)))
    elif elementType is 'Double':
        return row.setDouble(column,float(element))
    elif elementType is 'Bool':
        return row.setBoolean(column,bool(int(float(element))))
    elif elementType is 'Date':
        date = parse(element)
        return row.setDate(column,date.year,date.month,date.day)
    elif elementType is 'DateTime':
        date = parse(element)
        return row.setDateTime(column,date.year,date.month,date.day,date.hour,date.minute,date.second,date.microsecond)
    elif elementType is 'UnicodeString':
        return row.setString(column,element)
    else:
        return row.setCharString(column,element)

def detectBool(s):
    if s in ['True','true','1','False','false','0']:
        return True
    return False

def validPossibleType(element, possibleColumnType):
    if possibleColumnType in ['Double','Int']:  
        try:
            parsed2float = float(element)
            if possibleColumnType is 'Double':
                return True
            else:
                parsed2int = int(parsed2float)
                if parsed2float - parsed2int == 0:
                    return True
        except:
            return False

    elif possibleColumnType is 'Bool':
        return detectBool(element)

    elif possibleColumnType is 'UnicodeString':
        return True

    #Incompleto, no contempla todos los tipos
    else:
        return False

def chooseValidType(typesVector):
    
    possibleTypes = ['Bool','Int','Double','DateTime','Date','Duration','CharString','UnicodeString']

    for type in typesVector:
        if type == 'CharString' or type == 'UnicodeString':
            return 'UnicodeString'
        elif type == 'Duration':
            if 'Duration' in possibleTypes:
                possibleTypes = ['Duration']
            else:
                return 'UnicodeString'
        elif type == 'Date':
            if 'Date' in possibleTypes:
                possibleTypes = ['Date']
            else:
                return 'UnicodeString'
        elif type == 'DateTime':
            if 'DateTime' in possibleTypes:
                possibleTypes = ['DateTime']
            else:
                return 'UnicodeString'
        elif type == 'Double':
            if 'Double' in possibleTypes:
                possibleTypes = ['Double']
            else:
                return 'UnicodeString'
        elif type == 'Int':
            if 'Int' in possibleTypes:
                possibleTypes = ['Int','Double']
            else:
                possibleTypes = ['Double']
        else: 
            if 'Bool' in possibleTypes:
                possibleTypes = ['Bool','Int','Double']
            else:
                possibleTypes = ['Int','Double']
    return possibleTypes[0]


def createTable(numColumns):
    table = []
    for i in range(numColumns):
        table.append(['Bool','Int','Double','DateTime','Date','Duration','CharString','UnicodeString'])
    return table


def readCSV(csvFile,q):

    #csvReader = csv.reader(open(csvFile,'rb'),delimiter=',',quotechar='"')
    csvReader = csv.reader(open(csvFile,'rU'), dialect=csv.excel_tab, delimiter=',')

    while True:
        nextLine = next(csvReader,False)
        if nextLine:
            q.put(nextLine)
        else:
            q.put(False)
            break

    print "Termine de leer"

def typeIdentifier(q, cores):

    columns = q.get()
    numColumns = len(columns)

    pool = mp.Pool()
    freeCores = cores-2 # At least 2 cores are already being used by read and write processes

    computeLineParcial = partial(computeLine, q)

    results = pool.map(computeLineParcial, [numColumns for _ in range(freeCores)]) 

    results = zip(*results)

    types = []

    for result in results:
        types.append(chooseValidType(result)) # Falta implementar para que haga lo deseado

    return types

def chooseFirstValidType(typesVector):
    for type in typesVector:
        if type != '-':
            return type

def computeLine(q, numColumns):

    typesTable = createTable(numColumns)

    while True:
        nextLine = q.get()

        if not nextLine:
            q.put(False)
            break
        else:
            columnIndex = 0
            for object in nextLine:
                rowIndex = 0
                # Este for se podria hacer mas eficiente resolviendolo todo de una
                for possibleColumnType in typesTable[columnIndex]:
                    if possibleColumnType != '-' and not validPossibleType(object,possibleColumnType):
                        typesTable[columnIndex][rowIndex] = '-'                    
                    rowIndex = rowIndex + 1
                columnIndex = columnIndex + 1

    typesVector = []

    for i in range(numColumns):
        typesVector.append(chooseFirstValidType(typesTable[i]))

    return typesVector

def writeTDE(q,outputFileName, types):
    # Define type maps
    typesTable = {
        'Bool' :            tde.Type.BOOLEAN,
        'Int':              tde.Type.INTEGER,
        'Double':           tde.Type.DOUBLE,
        'Date':             tde.Type.DATE,
        'DateTime':         tde.Type.DATETIME,
        'Duration':         tde.Type.DURATION,
        'CharString':       tde.Type.CHAR_STRING,
        'UnicodeString':    tde.Type.UNICODE_STRING 
    }

    # Step 1: Create the Extract file and open the .csv

    tdefile = tde.Extract(outputFileName +'.tde')

    if tdefile.hasTable('Extract'):
        table = tdefile.openTable('Extract')
        tableDef = table.getTableDefinition()
        columns = q.get()
        numColumns = len(columns)

    else:
        # Step 2: Create the tableDef
        tableDef = tde.TableDefinition()
        columns = q.get()
        numColumns = len(columns)

        for i in range(numColumns):
            tableDef.addColumn(columns[i], typesTable[types[i]])

        # Step 3: Create the table in the image of the tableDef

        table = tdefile.addTable('Extract', tableDef)

    # Step 4: Loop through the csv, grab all the data, put it into rows
    # and insert the rows into  the table

    newrow = tde.Row(tableDef)

    while True:
        nextLine = q.get()

        if nextLine:
            for columnIndex in range(numColumns):
                insertRow(newrow,columnIndex, nextLine[columnIndex], types[columnIndex])        
            table.insert(newrow)
        else:
            break
    
    # Step 5: Close the tde

    tdefile.close()


def main():
    # Identify input
    if len(sys.argv) != 3:
        raise NameError('invalid arguments, valid input: python csv2tde.py inputFile outputFileName ')
    inputFile = sys.argv[1];
    outputFileName = sys.argv[2];

    # Create global variables

    try:
        cores = mp.cpu_count()
    except:
        cores = 4
 
    manager = mp.Manager()
    q1 = manager.Queue()

    # Check document format

    file_extension = os.path.splitext(inputFile)[1]

    if file_extension == '.csv':

        pRead = mp.Process(target=readCSV, args=(inputFile, q1,))

        pRead.start()

        types = typeIdentifier(q1,cores)

        q2 = manager.Queue()

        pRead = mp.Process(target=readCSV, args=(inputFile, q2,))

        pRead.start()

        writeTDE(q2, outputFileName, types)

    else:
        print 'Nos supported format, please use csv, json or xls' 


if __name__ == "__main__":
    main()
