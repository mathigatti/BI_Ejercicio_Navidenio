import unittest
from tdeConverter import *
from tdeConverterUtils import *

class chooseFirstValidType_TestCase(unittest.TestCase):

    def test_bool_is_first(self):
        dicc = {'Bool':True,'Int':False,'Double':True,'DateTime':True,'Date':False,'CharString':True,'UnicodeString':True}
        
        self.assertEqual(chooseFirstValidType(dicc),'Bool')

    def test_Date_is_first(self):
        dicc = {'Bool':False,'Int':False,'Double':False,'DateTime':False,'Date':True,'CharString':True,'UnicodeString':True}
        
        self.assertEqual(chooseFirstValidType(dicc),'Date')

class createTable_TestCase(unittest.TestCase):

    def test_Table_0_columns(self):
        self.assertEqual(createTable(0),[])

    def test_Table_1_column(self):
        res = [{'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}]
        
        self.assertEqual(createTable(1),res)

    def test_Table_4_columns(self):
        res = [{'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True, 'CharString':True,'UnicodeString':True},{'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True},{'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True},{'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}]
        self.assertEqual(createTable(4),res)

class validPossibleType_TestCase(unittest.TestCase):

    def test_TRUE_is_Bool_and_String(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':True,'Int':False,'Double':False,'DateTime':False,'Date':False,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'TRUE'),expectedRes)

    def test_1dot00_is_Double_and_String(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':False,'Int':False,'Double':True,'DateTime':False,'Date':False,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'1.0023'),expectedRes)

    def test_perro_is_only_String(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':False,'Int':False,'Double':False,'DateTime':False,'Date':False,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'perro'),expectedRes)

    def test_date(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':False,'Int':False,'Double':False,'DateTime':False,'Date':True,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'11/12/99'),expectedRes)

    def test_dateTime(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':False,'Int':False,'Double':False,'DateTime':True,'Date':False,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'11/12/99 11:24'),expectedRes)

    def test_decimal_with_ceros_is__int(self):
        options = {'Bool':True,'Int':True,'Double':True,'DateTime':True,'Date':True,'CharString':True,'UnicodeString':True}
        expectedRes = {'Bool':False,'Int':True,'Double':True,'DateTime':False,'Date':False,'CharString':True,'UnicodeString':True}
        self.assertEqual(validPossibleType(options,'42.00'),expectedRes)

class typeIdentifier_TestCase(unittest.TestCase):

    def test_Table_0_columns(self):
        reader = csv.reader(open('../testFiles/diasTest.csv','rU'), dialect=csv.excel_tab, delimiter=',')
        self.assertEqual(typeIdentifier(reader),['Int','Int','Int'])

class readerXLS_TestCase(unittest.TestCase):

    def test_iteration_XLS_file(self):
        xlsReader = ReaderXLS('../testFiles/test.xls','Hoja 1')
        expectedValue = [[u'c1', u'c2'], [1.0, 142.0], [1.0, 2.0], [3.0, 42.0], [2.0, 12.0], [4.0, 232.0]]

        res = []
        for i in xlsReader:
            res.append(i)

        self.assertEqual(res,expectedValue)

    def test_iteration_XLSX_file(self):
        xlsReader = ReaderXLS('../testFiles/test.xlsx','Hoja 1')
        expectedValue = [[u'c1', u'c2'], [1.0, 142.0], [1.0, 2.0], [3.0, 42.0], [2.0, 12.0], [4.0, 232.0]]

        res = []
        for i in xlsReader:
            res.append(i)

        self.assertEqual(res,expectedValue)


if __name__ == '__main__':
    unittest.main()