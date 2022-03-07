import os.path as path

from pathlib import Path
from dslib.helpers import replace_csv_header

current = Path(path.abspath(__file__)).parent


def create_path(p):
    return Path(current, p)


def create_data_file(data, header):
    """Create CSV file with header from file"""
    replace_csv_header(
        create_path(data),
        create_path(header),
    )
