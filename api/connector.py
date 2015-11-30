#/bin/env python

import mysql
from mysql.connector import errorcode
import json as json
from decimal import Decimal
import sys
import pdb
from datetime import date

from config import CONFIG

class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        pdb.set_trace()
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

class DB():
  config = CONFIG["db"]
  db = None
  cursor = None

  def __init__(self):
    try:
      self.db = mysql.connector.connect(**self.config)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err.msg)

    self.cursor = self.db.cursor(dictionary=True)

  def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.db.close()

  def query(self, query, json):
    self.cursor = self.db.cursor(dictionary=True)
    #print(query)
    try:
      self.cursor.execute(query)
    except mysql.connector.Error as err:
      print("Something went wrong")
      print(err.msg)
      return(str(0))

    result = self.cursor.fetchall()

    for item in result:
      for key in item.keys():
        if isinstance(item[key], Decimal):
          item[key] = float(item[key])
        if isinstance(item[key], date):
          item[key] = str(item[key])

    if json:
      if (CONFIG["debug"] == True):
        return json.dumps(result, sort_keys=True, indent=4)
      else:
        return json.dumps(result, cls=DecimalEncoder)
    else:
      return result
      
  def insert(self, query):
    self.db.cursor(dictionary=True)
    try:
      self.cursor.execute(query)
      self.db.commit()
    except mysql.connector.Error as err:
      print("Something went wrong")
      print(err.msg)
      return(str(0))

    return(self.cursor.lastrowid)

