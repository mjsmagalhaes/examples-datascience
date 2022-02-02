from zipfile import ZipFile


def unzip(file, dir):
  with ZipFile(file) as file:
    file.extractall(dir)


def human_format(num):
  num = float('{:.3g}'.format(num))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
