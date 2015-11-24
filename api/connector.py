#/bin/env python

import mysql
from mysql.connector import errorcode
import json
from decimal import Decimal
import sys

from config import CONFIG

class DecimalEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, Decimal):
      return float(o)
    return super(DecimalEncoder, self).default(o)

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

  def query(self, query):
    try:
      self.cursor.execute(query)
    except mysql.connector.Error as err:
      print("Something went wrong")
      print(err.msg)
      sys.exit(0);

    result = self.cursor.fetchall()
    if (CONFIG["debug"] == True):
      return json.dumps(result, sort_keys=True, indent=4, cls=DecimalEncoder)
    else:
      return json.dumps(result, cls=DecimalEncoder)

db = DB()

result = db.query("SELECT * FROM `settings`")

print(result)