from __future__ import annotations

import peewee

from typing import Union, List, Set, Tuple, Dict

# from IPython.display import display, Markdown as md
from itertools import chain
from more_itertools import take
from zipfile import ZipFile, ZIP_DEFLATED
from tqdm.notebook import trange, tqdm

from wow.query import Query, Predicate
from .encounter import Encounter
from .record import Record

EncounterDBProxy = peewee.DatabaseProxy()


class EncounterDB(peewee.Model):
    """
    """
    id = peewee.AutoField()
    # encounter_id = peewee.IntegerField()
    timestamp = peewee.TextField()
    event = peewee.TextField()
    # actor = peewee.TextField()
    rawdata = peewee.TextField()

    class Meta:
        database = EncounterDBProxy

    @ classmethod
    def save(cls, q: Query, idx, page_size=300):
        events = q.export()
        page = take(page_size, events)

        # print(len(events) / page_size)

        while page:
            cls.insert_many(page, fields=[
                cls.timestamp,
                cls.event,
                cls.rawdata
            ]).execute()

            page = take(page_size, events)


class Log:
    @ staticmethod
    def parse(file: str) -> Log:
        pBarComplete = tqdm(total=2)

        with open(file, 'r', encoding='utf-8') as filePtr:
            lines = filePtr.readlines()
            pBarLoading = tqdm(total=len(lines), desc='Loading')

            def transform(x):
                pBarLoading.update()
                return Record(x)

            log = Query(
                enumerate(lines)
            ).map(
                transform
            ).qlist()

        pBarComplete.update()

        # Split Encounters
        encounters = Query(zip(
            log.filter(Predicate.isEncounterStart()),
            log.filter(Predicate.isEncounterEnd())
        )).map(
            lambda x: Encounter(log, x[0], x[1])
        ).filter(
            lambda x: x.duration.total_seconds() > 60
        ).list()

        pBarComplete.update()

        print('Encounters: ', len(encounters))

        l = Log(log, encounters)

        pBarComplete.update()

        return l

    def __init__(self, log, encounters: List[Encounter]):
        self.log = log
        self.encounters = encounters

    def save_encounters(self, page_size=300) -> None:
        events = Query(chain(*self.encounters)).map(
            (
                Predicate.getTimestampString(),
                Predicate.getEvent(),
                Predicate.getRawData()
            )
        ).iter()

        file = self.encounters[0].timestamp_begin.strftime(
            'encounters_%Y_%m_%d')
        filePath = f'wow/{file}.db'
        zipPath = f'wow/{file}.zip'

        with peewee.SqliteDatabase(filePath) as db:
            EncounterDBProxy.initialize(db)
            EncounterDB.create_table()
            with db.atomic():
                page = take(page_size, events)

                while page:
                    EncounterDB.insert_many(page, fields=[
                        EncounterDB.timestamp,
                        EncounterDB.event,
                        EncounterDB.rawdata
                    ]).execute()

                    page = take(page_size, events)

        with ZipFile(zipPath, 'w', compression=ZIP_DEFLATED, compresslevel=6) as z:
            z.write(filePath)
