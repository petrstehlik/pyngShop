#/bin/env python

import mysql
from mysql.connector import errorcode
import json
import itertools

CONFIG = {
	'user' : 'pyngshop',
	'database' : 'pyngshop',
	'password' : 'klobaska',
	'port' : 8889
}

try:
  cnx = mysql.connector.connect(**CONFIG)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
cursor = cnx.cursor()

def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()]

TABLES = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

try:
	#print("Creating table employees: ", end='')
	#cursor.execute(TABLES)
  cursor.execute("SELECT * FROM `category`")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
		print("already exists.")
	else:
		print(err.msg)
else:
	print("OK")

result = dictfetchall(cursor)
for item in result:
  print str(item)
  print("================")
  for col in item:
    print str(col)
#print(result[0])


cursor.close()
cnx.close()
