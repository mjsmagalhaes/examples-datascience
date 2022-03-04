from __future__ import annotations


import pandas as pd
import datatable as dt
import datetime as date

from functools import reduce
# from itertools import groupby,
from more_itertools import ilen, islice_extended, groupby_transform
from typing import Any, Dict, Set, Union, List, Tuple, Callable

FilterPredicate = Callable[[Any], bool]

MapFunction = Callable[[Any], Any]
MapPredicate = Union[MapFunction, List[MapFunction], Tuple[MapFunction]]


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


class Predicate:
    """
    A factory of predicates used in Query.
    """

    # === FILTER Predicates ===

    @staticmethod
    def any(fns):
        return lambda x: any(map(lambda f: f(x), fns))

    @staticmethod
    def all(fns):
        return lambda x: all(map(lambda f: f(x), fns))

    @staticmethod
    def isActionCompound() -> FilterPredicate:
        return lambda r: type(r['action_e1']) == list

    # --- FILTER Predicates: Target ---

    @staticmethod
    def isTarget(target) -> FilterPredicate:
        return lambda x: x.target == target

    @staticmethod
    def isTargetHostile() -> FilterPredicate:
        return lambda x: x.target_mask.hostile == True

    # --- FILTER Predicates: Actor ---

    @staticmethod
    def isActor(actor) -> FilterPredicate:
        return lambda x: x.actor == actor

    @staticmethod
    def isActorHostile() -> FilterPredicate:
        return lambda x: x.actor_mask.hostile == True

    # --- FILTER Predicates: Actions ---

    @staticmethod
    def isAction(action) -> FilterPredicate:
        return lambda x: x.action == action

    @staticmethod
    def isActionId(id: int) -> FilterPredicate:
        return lambda x: x.action_id == id

    @staticmethod
    def isPlayerAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Player' and x.actor != '0'

    def isPetAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Pet' and x.actor != '0'

    @staticmethod
    def isCreatureAction() -> FilterPredicate:
        return lambda x: x.actor_tag == 'Creature'

    # --- FILTER Predicates: Events ---
    @staticmethod
    def isEventIn(event_list: List[str]) -> FilterPredicate:
        return lambda x: x.event in event_list

    @classmethod
    def isEncounterStart(cls) -> FilterPredicate:
        return cls.isEventIn(['ENCOUNTER_START'])

    @classmethod
    def isEncounterEnd(cls) -> FilterPredicate:
        return cls.isEventIn(['ENCOUNTER_END'])

    # === MAP Predicates ===

    @staticmethod
    def getData() -> MapPredicate:
        return lambda x: x.data

    @staticmethod
    def getDataIndex(idx) -> MapPredicate:
        return lambda x: x.data[idx]

    @staticmethod
    def getRawData() -> MapPredicate:
        return lambda x: x.rawdata

    @staticmethod
    def getEvent() -> MapPredicate:
        return lambda x: x.event

    @staticmethod
    def getTimestamp() -> MapPredicate:
        return lambda x: x.getTimestamp()

    @staticmethod
    def getTimestampString() -> MapPredicate:
        return lambda x: x.getTimestampString()

    # --- MAP Predicates: Actor ---

    @staticmethod
    def getActor() -> MapPredicate:
        return lambda x: x.actor

    @staticmethod
    def getActorTag() -> MapPredicate:
        return lambda x: x.actor_tag

    @staticmethod
    def getActorId() -> MapPredicate:
        return lambda x: x.actor_id

    @staticmethod
    def getActorFlags() -> MapPredicate:
        return lambda x: x.actor_flags

    @classmethod
    def getActorInfo(cls) -> MapPredicate:
        return (
            cls.getActor(),
            cls.getActorTag(),
            cls.getActorId()
        )

    # --- MAP Predicates: Target ---

    @staticmethod
    def getTarget() -> MapPredicate:
        return lambda x: x.target

    @staticmethod
    def getTargetTag() -> MapPredicate:
        return lambda x: x.target_tag

    @staticmethod
    def getTargetId() -> MapPredicate:
        return lambda x: x.target_id

    @staticmethod
    def getTargetFlags() -> MapPredicate:
        return lambda x: x.target_flags

    @classmethod
    def getTargetInfo(cls) -> MapPredicate:
        return (
            cls.getTarget(),
            cls.getTargetTag(),
            cls.getTargetId()
        )

    # --- MAP Predicates: Actions ---

    @staticmethod
    def getAction() -> MapPredicate:
        return lambda x: x.action

    @staticmethod
    def getActionId() -> MapPredicate:
        return lambda x: x.action_id
