import os.path as path

from pathlib import Path
from dslib.helpers import replace_csv_header


def create_path(p, reference=__file__):
    ref = Path(path.abspath(reference))

    return Path(
        ref.parent if ref.is_file() else ref,
        p
    )


def create_data_file(data, header):
    """Create CSV file with header from file"""
    replace_csv_header(
        create_path(data),
        create_path(header),
    )
