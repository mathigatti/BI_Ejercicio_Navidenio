# BI_EjercicioNavidenio

tdeConverter is a program that converts CSV and XLS format files to TDE files (Tableau format). It infers the type of values of the columns in the given file so there is no need to give this information manually. An important requirement to get it working is to format the inputfile with the first row indicating the names of each column.


Requirements:

	* Python 2.7.X
	* Tableau SDK https://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_installing.htm#downloading
	* Some python libraries: csv, xlrd, time and dateutil

Files in the repository

* In src you can access to the converter and its unit tests.

	- To get started you can type: 
		python tdeConverter.py ../testFiles/test.csv
	- it should create the tde file version of test.csv in TDEs.

* testFiles contains some example files, which where used to test the converter.

* TDEs is the default path for new generated TDEs
