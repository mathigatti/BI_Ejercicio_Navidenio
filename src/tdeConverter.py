#######################################################################################################
# Examples of usage and expected output values are documented with unit tests in test_tdeConverter.py #
#######################################################################################################

import sys
import os

from time import gmtime, strftime
from tdeConverterUtils import *

root = '../TDEs/'

def createTDE(outputFileName,reader,types):
    tdefile = tde.Extract(outputFileName +'.tde')

    if tdefile.hasTable('Extract'):
        table = tdefile.openTable('Extract')
        tableDef = table.getTableDefinition()
        columns = reader.next()
        numColumns = len(columns)
    else:
        tableDef = tde.TableDefinition()
        columns = reader.next()
        numColumns = len(columns)

        for i in range(numColumns):
            tableDef.addColumn(columns[i], typesDict[types[i]].tdeType)

        table = tdefile.addTable('Extract', tableDef)

    return table, tableDef, numColumns, tdefile


def xls2tde(inputFile, sheetName):

    xlsReader = ReaderXLS(inputFile,sheetName)

    # Infer type of each column in the file
    types = typeIdentifier(xlsReader)

    xlsReader = ReaderXLS(inputFile,sheetName)

    outputFileName = strftime(root + "XLS_%Y-%m-%d_%H:%M:%S", gmtime())

    # Create TDE file, its table with its columns and labels
    table, tableDef, numColumns, tdefile = createTDE(outputFileName, xlsReader,types)

    newrow = tde.Row(tableDef)

    # Insert rows
    for line in xlsReader:
        for columnIndex in range(numColumns):
            insertRow(newrow,columnIndex, line[columnIndex], types[columnIndex])        
        table.insert(newrow)

    tdefile.close()


def csv2tde(csvFile):

    csvReader = readCSV(csvFile)

    # Infer type of each column in the file
    types = typeIdentifier(csvReader)

    csvReader = readCSV(csvFile)

    outputFileName = strftime(root + "CSV_%Y-%m-%d_%H:%M:%S", gmtime())

    # Create TDE file, its table with its columns and labels
    table, tableDef, numColumns, tdefile = createTDE(outputFileName, csvReader, types)

    newrow = tde.Row(tableDef)

    # Insert rows
    for line in csvReader:
        for columnIndex in range(numColumns):
            insertRow(newrow,columnIndex, line[columnIndex], types[columnIndex])        
        table.insert(newrow)

    tdefile.close()


def main():
    global typesDict

    # Identify input
    if len(sys.argv) < 2:
        raise NameError('invalid arguments, valid input: python tdeConverter.py inputFile XLS_SheetName(optional)')
    inputFile = sys.argv[1];
    file_extension = os.path.splitext(inputFile)[1]

    # CSV
    if file_extension == '.csv':
        csv2tde(inputFile)

    # XLS or XLSX
    elif file_extension == '.xls' or file_extension == '.xlsx':
        if len(sys.argv) < 3:
            raise NameError('invalid arguments, valid input: python tdeConverter.py XLSinputFile XLS_SheetName')
        else:
            xls2tde(inputFile,sys.argv[2])

    # Invalid Input
    else:
        print 'Not supported format, please use csv or xls' 


if __name__ == "__main__":
    main()
