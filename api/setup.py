#/bin/env python

import _mysql
from _mysql_exceptions import *
#from _mysql.connector import errorcode
import json
import itertools
import sys

from config import CONFIG



class DB():
  config = CONFIG
  db = 0

  def __init__(self):
    try:
      self.db = _mysql.connect(**self.config)
    except OperationalError as err:
      print("Something went wrong")
      print(err)
      sys.exit(0)

  def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

  def query(self, query):
    self.db.query(query)
    print(query)

    try:
      r = self.db.store_result()
    except ProgrammingError as err:
      print("Blbe!")
      sys.exit(0);

    result = r.fetch_row(0)
    return result

db = DB()

print(db.db)
  
try:
  res = db.query("""SELECT * FROM `product`""")
except ProgrammingError as err:
  print("Blbe!")
  sys.exit(0)


print(res)

#result = dictfetchall(cnx)
"""for item in result:
  print(str(item))
  print("================")
  for col in item:
    print(str(col))"""
#print(result[0])
