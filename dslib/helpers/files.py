import pandas as pd

from os import path
from zipfile import ZipFile, ZIP_DEFLATED

# tokens_to_remove = ['/n']


def replace_csv_header(dataFile, headerFile, csvFile=None, header=None):
    """
    Create a CSV file by replacing the original header (even if empty) with a new header contained in the headerFile.

    The headerFile must have a column name per line.

    header is usually None or the first row. Passed directly to pandas.read_csv.
    """

    with open(headerFile) as f:
        var_names = f.readlines()

    data = pd.read_csv(dataFile, header=header)

    # remove /n from column names
    data.columns = list(
        map(lambda s: s.replace('\n', ''), var_names)
    )

    if csvFile is None:
        p = path.splitext(headerFile)
        csvFile = p[0] + '.csv'

    data.to_csv(csvFile)


def unzip(file, dir):
    with ZipFile(file) as file:
        file.extractall(dir)


def zip(zipPath, filePath):
    with ZipFile(zipPath, 'w', compression=ZIP_DEFLATED, compresslevel=6) as z:
        z.write(filePath)
