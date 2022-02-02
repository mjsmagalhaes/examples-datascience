from __future__ import annotations

import datetime as date

from IPython.display import display, Markdown as md
from itertools import chain
from more_itertools import ilen
from typing import Union, List, Set, Tuple, Dict

from wow import ENCOUNTER_DATA
from wow.query import Query, Predicate

# https://wowpedia.fandom.com/wiki/DifficultyID

cDifficulty = {
    '7': 'LFR',
    '14': 'Normal',
    '15': 'Heroic',
    '16': 'Mythic'
}


class Mask:
  def __init__(self, flags):
    self.flags = self.hex_to_binary(flags)

  def hex_to_binary(self, hex_number: str, num_digits: int = 64) -> str:
    """
    Converts a hexadecimal value into a string representation
    of the corresponding binary value.

    Args:
      hex_number: str hexadecimal value
      num_digits: integer value for length of binary value.
                    defaults to 8

    Returns:
      string representation of a binary number 0-padded
      to a minimum length of <num_digits>
    """
    return bin(int(hex_number, 16))[2:].zfill(num_digits)[::-1]

  @property
  def hostile(self):
    return self.flags[6] == '1'


class Record:
  """
  Represents a line in the log file.
  """

  def __init__(self, log: Tuple[int, str]):
    self.idx = log[0]
    self.timestamp, self.rawdata = log[1].split('  ')

    # if(self.event in [
    #     'COMBAT_LOG_VERSION', 'ZONE_CHANGE', 'MAP_CHANGE',
    #     'COMBATANT_INFO',
    #     'UNIT_DIED', 'PARTY_KILL',
    #     'ENCOUNTER_START', 'ENCOUNTER_END',
    #     'WORLD_MARKER_PLACED', 'WORLD_MARKER_REMOVED',
    #     'EMOTE'
    # ]):

  # def __str__(self) -> str:
  #   return '{timestamp}: {event}'.format(**self.__dict__)

  def __repr__(self) -> str:
    return f'{self.idx} - {self.timestamp}: {self.rawdata}'

  def __getitem__(self, idx):
    if type(idx) is str:
      return self.__dict__.get(idx, None)
    if type(idx) is int:
      try:
        return self.data[idx]
      except IndexError:
        return None
    else:
      return None

  @property
  def data(self):
    return self.rawdata.split(',')

  @property
  def event(self):
    return self[0]

  @property
  def actor_id(self):
    return self[1]

  @property
  def actor(self):
    return self[2]

  @property
  def actor_flags(self):
    return self[3]

  @property
  def actor_tag(self) -> Mask:
    return self.actor_id.split('-')[0]

  @property
  def actor_mask(self) -> Mask:
    return Mask(self.actor_flags)

  @property
  def target_id(self):
    return self[5]

  @property
  def target(self):
    return self[6]

  @property
  def target_flags(self):
    return self[7]

  @property
  def target_tag(self) -> Mask:
    return self.target_id.split('-')[0]

  @property
  def target_mask(self) -> Mask:
    return Mask(self.target_flags)

  @property
  def action_id(self) -> int:
    r = self[9]
    if r:
      return int(r)
    else:
      return None

  @property
  def action(self) -> str:
    return self[10]


class Encounter:
  """
  Represents a group of Records in a single Encounter.

  A encounter starts with the event ENCOUNTER_START and finishes with a ENCOUNTER_END event.
  """

  @staticmethod
  def parse(file: str) -> Tuple[Query, List[Encounter]]:
    with open(file, 'r', encoding='utf-8') as filePtr:
      log = Query(
          enumerate(filePtr.readlines())
      ).map(
          lambda x: Record(x)
      ).qlist()

    # Split Encounters
    encounters = Query(zip(
        log.filter(Predicate.isEncounterStart()),
        log.filter(Predicate.isEncounterEnd())
    )).map(
        lambda x: Encounter(log, x[0], x[1])
    ).filter(
        lambda x: x.duration.total_seconds() > 60
    ).list()

    print('Encounters: ', len(encounters))

    return (log, encounters)

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

## <sb>{0.difficulty} {0.name} {0.result} (id: {0.id})</sb>
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

    return self.q.filter(
        Predicate.isPlayerAction()
    ).map(
        Predicate.getActorInfo()
    ).set()

  def listEncounters(self):
    return self.q.filter(Predicate.isEncounterStart()).list()

  def showEncounters(self):
    for e in self.data:
      display(e.md())

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
        Predicate.isEvent(event)  # 'SPELL_AURA_APPLIED'
    ).filter(
        Predicate.isAction(action)  # '"Sorrowful Procession"'
    ).map(
        (
            Predicate.getTimestamp(),
            Predicate.getActorId(),
            Predicate.getTarget()
        )
    )

  @classmethod
  def groupActionByActor(self, event, action) -> Dict[str, Tuple]:
    return self.actions(self.q, event, action).groupby(
        lambda x: x[1],
        lambda x: x[2],
    ).dict()
