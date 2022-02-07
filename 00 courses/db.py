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

  def __enter__():
    pass

  def __init__():
    pass
