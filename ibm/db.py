import ibm_db

from typing import Dict


class ibmdb:
  def __init__(self, credentials: Dict) -> None:
    dsn = (
        "DRIVER={0};"
        "DATABASE={database};"
        "HOSTNAME={hostname};"
        "PORT={port};"
        "PROTOCOL={1};"
        "UID={username};"
        "PWD={password};"
        "SECURITY={2};").format("{IBM DB2 ODBC DRIVER}", "TCPIP", 'SSL', **credentials)

    try:
      self.conn = ibm_db.connect(dsn, "", "")
      print((
          "Connected to database:{database} "
          "as user: {username} "
          "on host: {hostname}"
      ).format(**credentials))
    except:
      print("Unable to connect: ", ibm_db.conn_errormsg())
      raise Exception('BOOM.')

  def createTable(self, name):
    dropQuery = f"drop table {name};"

    try:
      ibm_db.exec_immediate(self.conn, dropQuery)
    finally:
      createQuery = (
          f"create table {name}("
          "id INTEGER PRIMARY KEY NOT NULL,"
          "fname VARCHAR(20),"
          "lname VARCHAR(20),"
          "city VARCHAR(20),"
          "ccode CHAR(2)"
          ")"
      )

      # Now fill in the name of the method and execute the statement
      createStmt = ibm_db.replace_with_name_of_execution_method(
          self.conn,
          createQuery
      )

  def insertData(self):
    insertQuery2 = "insert into INSTRUCTOR values (2, 'Raul', 'Chong', 'Markham', 'CA'), (3, 'Hima', 'Vasudevan', 'Chicago', 'US')"
    insertStmt2 = ibm_db.exec_immediate(self.conn, insertQuery2)

  def selectData(self):
    selectQuery = "select * from INSTRUCTOR;"
    # Execute the statement
    selectStmt = ibm_db.exec_immediate(self.conn, selectQuery)

    # Fetch the Dictionary (for the first row only)
    ibm_db.fetch_both(selectStmt)
    # Fetch the rest of the rows and print the ID and FNAME for those rows
    while ibm_db.fetch_row(selectStmt) != False:
      print(" ID:",  ibm_db.result(selectStmt, 0),
            " FNAME:",  ibm_db.result(selectStmt, "FNAME"))

  def __enter__():
    pass

  def __leave__():
    pass
