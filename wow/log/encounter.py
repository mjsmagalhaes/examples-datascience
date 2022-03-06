from __future__ import annotations
from typing import Union, List, Tuple, Set, Dict

from datetime import date

from IPython.display import display, Markdown as md
from itertools import chain
from rich.table import Table
from rich.console import Console

from wow import SPECIALIZATION_DATA, CLASS_DATA, ENCOUNTER_DATA, cDifficulty
from wow.query import Query, Predicate

from .record import Record


class Encounter:
    """
    Represents a group of Records in a single Encounter.

    A encounter starts with the event ENCOUNTER_START and finishes with a ENCOUNTER_END event.
    """

    def from_db() -> List[Encounter]:
        pass

    def __init__(self, log: Query, beg: Record, end: Record):
        self.beg = beg
        self.timestamp_begin = date.datetime.strptime(
            beg.timestamp, '%m/%d %H:%M:%S.%f'
        ).replace(year=2022)

        self.end = end
        self.timestamp_end = date.datetime.strptime(
            end.timestamp, '%m/%d %H:%M:%S.%f'
        ).replace(year=2022)

        try:
            self.id = int(beg.data[1])
            self.name = beg.data[2]
        except:
            print(beg)
            raise Exception('BOOM.')

        self.log = log.slice(self.beg.idx, self.end.idx + 1).qlist()

    def __repr__(self) -> str:
        return self.text

    def __iter__(self):
        return self.iter()

    @property
    def q(self) -> Query:
        return self.log

    # NOTE: There is a minor difference in miliseconds between
    # duration (calculated from encounter_start / encounter_end timestamp) and
    # log_duration (extracted from the log)
    @property
    def duration(self) -> date.timedelta:
        return self.timestamp_end - self.timestamp_begin

    @property
    def log_duration(self):
        return str(
            date.timedelta(microseconds=int(self.end[6]) * 1000)
        )

    @property
    def title(self) -> str:
        return f'{self.name} {self.duration.seconds // 60}:{self.duration.seconds % 60:02d}'

    @property
    def text(self):
        return """
<style>
sb {{ color: steelblue }}
o {{ color: Orange }}
g {{ color: Green }}
</style>

# <sb>{0.difficulty} {0.name} {0.result} (id: {0.id})</sb>
- {0.beg}
- {1} entries in **{0.log_duration}** / {0.duration}
- {0.end}
""".format(self, self.q.len())

    @property
    def difficulty(self):
        return cDifficulty.get(self.beg[3], None)

    @property
    def result(self) -> str:
        return ['Wipe', 'Kill'][int(self.end[5])]

    def md(self):
        display(md(self.text))

    def iter(self):
        return self.q.iter()

    def getReport(self) -> EncounterReport:
        return ENCOUNTER_DATA.get(self.id, EncounterReport)(self)

    def export(self) -> List[Tuple[str, str, str]]:
        return self.q.map(
            (
                Predicate.getTimestampString(),
                Predicate.getEvent(),
                Predicate.getRawData()
            )
        ).iter()


class EncounterReport:
    """
    A pré-defined Query
    """

    def __init__(self, encounters: Union[Encounter, List[Encounter], Tuple[Encounter], Query]) -> None:
        if type(encounters) in [list, tuple]:
            self.data = encounters
        else:
            self.data = [encounters]

    @property
    def q(self):
        return Query(chain(*self.data))

    @property
    def e(self):
        if(len(self.data) == 1):
            return self.data[0]
        else:
            return None

    def report(self):
        self.showEncounters()

    def listPlayers(self) -> Set:
        """
        Returns a set with all players in the fight
        """
        playerSpec = self.q.filter(
            Predicate.isEventIn(['COMBATANT_INFO'])
        ).map(
            (
                Predicate.getActorId(),
                Predicate.getDataIndex(24)
            )
        ).dict()

        players = Table(title="Players")
        players.add_column("Name")
        players.add_column("ID")
        players.add_column("Class")
        players.add_column("Spec")
        players.add_column("Role")

        # print(playerData)

        playerList = self.q.filter(
            Predicate.isPlayerAction()
        ).map(
            Predicate.getActorInfo()
        ).set()

        playerData = {}

        for p in playerList:
            name, _, id = p

            specID = playerSpec[id]

            className, specName, role = SPECIALIZATION_DATA[int(specID)]
            color = CLASS_DATA[className]

            playerData.update(
                {id: (name, id, className, specName, role, color)})

        for p in sorted(playerData.items(), key=lambda p: '{0}-{1}-{2}'.format(p[1][4], p[1][2], p[1][4])):
            name, id, className, specName, role, color = p[1]
            players.add_row(name, id, className, specName, role, style=color)

        Console().print(players)

        return playerList

    def listEncounters(self):
        return self.q.filter(Predicate.isEncounterStart()).list()

    def showEncounters(self):
        for e in self.data:
            display(e.md())

    def getSpellDamage(self):
        spellDamage = self.q.filter(
            Predicate.all([
                Predicate.any([Predicate.isPlayerAction(),
                               Predicate.isPetAction()]),
                Predicate.isTargetHostile(),
                Predicate.isEventIn([
                    'SPELL_DAMAGE',
                    'SPELL_PERIODIC_DAMAGE',
                    'RANGE_DAMAGE'
                ]),
            ])
        ).map((
            Predicate.getActorId(),
            Predicate.getActor(),
            lambda x: int(x[29])
        )).groupby(
            lambda x: tuple(x[0:2]),
            lambda x: x[2],
            # lambda x: help.human_format(sum(x))
            sum
        ).sort(
            lambda x: x[1],
            True
        ).map(
            lambda x: (*x[0], x[1])  # help.human_format(x[1])
        ).pandas(['Unit ID', 'Name', 'Total (Spell)'])

        return spellDamage

    def getMeleeDamage(self):
        def consolidate(x):
            return [x.action, x.actor_id][x.action[0:3] == '000']

        meleeDamage = self.q.filter(
            Predicate.all([
                Predicate.any([Predicate.isPlayerAction(),
                               Predicate.isPetAction()]),
                Predicate.isTargetHostile(),
                Predicate.isEventIn([
                    'SWING_DAMAGE',
                ]),
            ])
        ).map(
            (
                Predicate.getActorId(),
                consolidate,
                Predicate.getActor(),
                lambda x: int(x[26])
            )
        ).groupby(
            lambda x: tuple(x[0:3]),
            lambda x: x[3],
            # lambda x: help.human_format(sum(x))
            sum
        ).sort(
            lambda x: x[1],
            True
        ).map(
            lambda x: (*x[0], x[1])  # help.human_format(x[1])
        ).pandas(['Unit ID', 'Player ID', 'Name', 'Total (Melee)'])

        return meleeDamage

    def getDamage(self):
        return (
            self.getSpellDamage(),
            self.getMeleeDamage()
        )

    def hostile_action(self) -> Query:
        # Hostile NPCs & Their Actions
        return self.q.filter(
            Predicate.isCreatureAction()
        ).filter(
            Predicate.isActorHostile()
        ).map(
            (Predicate.getActor(), Predicate.getEvent(), Predicate.getAction())
        ).groupby(
            lambda x: x[0],
            lambda x: x[1],
            set
        ).dict()

    def hostile_action2(self) -> Query:
        return self.q.filter(
            Predicate.isCreatureAction()
        ).filter(
            Predicate.isActorHostile()
        ).map(
            (Predicate.getActionId(), Predicate.getAction(),
             Predicate.getActor(), Predicate.getEvent())
        ).qset(
        ).sort(
            lambda x: x[1]
        ).list()

    def actor_actions(self, actor) -> Query:
        return self.q.filter(
            Predicate.isActor(actor)
        ).map(
            (
                Predicate.getAction(),
                Predicate.getEvent(),
                Predicate.getTarget()
            )
        )

    def actions(self, event, action) -> Query:
        return self.q.filter(
            Predicate.isEventIn(event)  # 'SPELL_AURA_APPLIED'
        ).filter(
            Predicate.isAction(action)  # '"Sorrowful Procession"'
        ).map(
            (
                Predicate.getTimestamp(),
                Predicate.getActorId(),
                Predicate.getTarget()
            )
        )

    @ classmethod
    def groupActionByActor(self, event, action) -> Dict[str, Tuple]:
        return self.actions(self.q, event, action).groupby(
            lambda x: x[1],
            lambda x: x[2],
        ).dict()
