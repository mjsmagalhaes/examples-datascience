from __future__ import annotations


import pandas as pd
import datatable as dt
import datetime as date

from typing import Union, Dict, Set, List, Tuple

from functools import reduce
from more_itertools import ilen, islice_extended, groupby_transform

from .predicate import MapFunction, FilterPredicate


class Query:
    """
    A class to create a chain of iterators to help the analysis.
    """

    def __init__(self, data):
        # print('New Query')
        self.data = data

    def __iter__(self):
        return self.iter()

    def iter(self):
        return iter(self.data)

    def apply(self, fn1, fn2: MapFunction, data) -> Query:
        """
        This function should'nt be called directly.
        """
        return Query(fn1(fn2, data))

    def map(self, fn):
        """
        A wrapper around default map function to create a chainable interface.

        Args:
          fn: function | tuple / list - function or group of funcions that will be 
              called to map each entry.
        """
        if type(fn) in [list, tuple]:

            def new_fn(x):
                return tuple(map(lambda f: f(x), fn))

            return self.apply(map, new_fn, self.iter())
        else:
            return self.apply(map, fn, self.iter())

    def filter(self, fn: FilterPredicate) -> Query:
        """
        A wrapper around default filter function to create a chainable interface.

        Args:
          fn: function - function that will be called to filter entries.

        Returns:
          The iterator wrapped in a Query object.
        """

        return self.apply(filter, fn, self.iter())

    def groupby(self, keyfn, valuefn=None, reducefn=list) -> Query:
        """
        A wrapper around itertools.groupby function to create a chainable interface.

        Args:
          key: A function that will be called to determine by which value entries will be grouped by.

        Returns:
          The iterator wrapped in a Query object.
        """
        return Query(groupby_transform(self.sort(keyfn).iter(), keyfn, valuefn, reducefn))

    def slice(self, start=0, stop=None, step=1):
        return Query(islice_extended(self.iter(), start, stop, step))

    def sort(self, key=None, reverse=False):
        return Query(sorted(self.iter(), key=key, reverse=reverse))

    # --- Semi-Finalizers ---

    def qlist(self):
        return Query(self.list())

    def qset(self):
        return Query(self.set())

    def reduce(self, fn):
        return reduce(fn, self.iter())

    # --- Finalizers ---

    def set(self) -> Set:
        return set(self.iter())

    def list(self) -> List:
        return list(self.iter())

    def tuple(self) -> Tuple:
        return tuple(self.iter())

    def dict(self) -> Dict:
        return dict(self.iter())

    def pandas(self, columns: Union[List[str], None] = None) -> pd.DataFrame:
        """
        Transform the iterator in this object into a Pandas DataFrame

        Args:
          columns: columns names or None.

        Returns:
          A Pandas DataFrame
        """
        return pd.DataFrame(self.iter(), columns=columns)

    def datatable(self, columns: Union[List[str], None] = None) -> dt.Frame:
        """
        Transform the iterator in this object into a Datatable Frame.

        Args:
          columns: columns names or None.

        Returns:
          A Datatable Frame
        """
        return dt.Frame(self.pandas(columns=columns))

    def len(self):
        return ilen(self.iter())
