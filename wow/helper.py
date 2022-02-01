from zipfile import ZipFile


def unzip(file, dir):
  with ZipFile(file) as file:
    file.extractall(dir)
