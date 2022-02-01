from __future__ import annotations

import datetime as date

from IPython.display import display, Markdown as md
from itertools import islice
from more_itertools import ilen
from typing import List, Set, Tuple

from .query import Query, Predicate


class Mask():
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
    # self.data = data.split(',')
    # data = data.split(',')
    # self.event = data[0]

    if(self.event in [
        'COMBAT_LOG_VERSION', 'ZONE_CHANGE', 'MAP_CHANGE',
        'COMBATANT_INFO',
        'PARTY_KILL',
        'ENCOUNTER_START', 'ENCOUNTER_END',
        'WORLD_MARKER_PLACED', 'WORLD_MARKER_REMOVED',
        'EMOTE'
    ]):
      return
    # elif self.event in ['ENCOUNTER_START']:
    #   self.data = data
    elif self.event in ['UNIT_DIED']:
      self.parse_actor()
      self.parse_target()
    else:
      try:
        self.parse_actor()
        self.parse_target()
        self.parse_action()
      except:
        print(log)
        raise Exception('BOOM.')

  def __str__(self) -> str:
    return '{timestamp}: {event}'.format(**self.__dict__)

  def __repr__(self) -> str:
    return '{timestamp}: {event} entry: {idx}'.format(**self.__dict__)

  def __getitem__(self, idx):
    if type(idx) is str:
      return self.__dict__.get(idx, None)
    if type(idx) is int:
      return self.data[idx]
    else:
      return None

  @property
  def data(self):
    return self.rawdata.split(',')

  @property
  def event(self):
    return self.data[0]

  @property
  def actor_id(self):
    return self.data[1]

  @property
  def actor(self):
    return self.data[2]

  @property
  def actor_flags(self):
    return self.data[3]

  @property
  def actor_tag(self) -> Mask:
    return self.actor_id.split('-')[0]

  @property
  def actor_mask(self) -> Mask:
    return Mask(self.actor_flags)

  @property
  def target_id(self):
    return self.data[5]

  @property
  def target(self):
    return self.data[6]

  @property
  def target_flags(self):
    return self.data[7]

  @property
  def target_tag(self) -> Mask:
    return self.target_id.split('-')[0]

  @property
  def target_mask(self) -> Mask:
    return Mask(self.target_flags)

  @property
  def action_id(self):
    return self.data[9]

  @property
  def action(self):
    return self.data[10]

  def parse_actor(self):
    pass
    # self.actor_id, self.actor = data[1:3]
    # self.actor_flags = data[3]
    # self.actor_marks = bin(int(self.data[4], 16))[2:].zfill(64)[::-1]
    # self.actor_tag, *_ = self.actor_id.split('-')

  def parse_target(self):
    pass
    # self.target_id, self.target = self.data[5:7]
    # self.target_flags = self.data[7]
    # self.target_marks = bin(int(self.data[8], 16))[2:].zfill(64)[::-1]
    # self.target_tag, *_ = self.target_id.split('-')

  def parse_action(self):
    pass
    # self.action_id, self.action, *self.action_e1 = self.data[9:]


class Encounter:
  """
  Represents a group of Records in a single Encounter.

  A encounter starts with the event ENCOUNTER_START and finishes with a ENCOUNTER_END event.
  """

  @staticmethod
  def parse(file: str) -> Tuple[Query, List[Encounter]]:  # List[Record]
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

    self.duration = self.timestamp_end - self.timestamp_begin

    try:
      self.id = int(beg.data[1])
      self.name = beg.data[2]
    except:
      print(beg)
      raise Exception('BOOM.')

    self.log = log.slice(self.beg.idx, self.end.idx + 1).qlist()

  def __repr__(self) -> str:
    return self.text()

  def __iter__(self):
    return self.iter()

  def title(self) -> str:
    return f'{self.name} {self.duration.seconds // 60}:{self.duration.seconds % 60:02d}'

  def text(self):
    return """
<style>
sb {{ color: steelblue }}
o {{ color: Orange }}
g {{ color: Green }}
</style>

## <sb>{name} (id: {id})</sb>
- {beg.event} (log: {beg.idx})
  - *{timestamp_begin}*  
- {0} entries in **{duration}**
- {end.event} (log: {end.idx})
  - *{timestamp_end}*
    """.format(ilen(self.iter()), **self.__dict__)

  def md(self):
    display(md(self.text()))

  @property
  def q(self):
    return self.log

  def iter(self):
    return islice(self.q.iter(), self.beg.idx, self.end.idx + 1)

  @property
  def players(self) -> Query:
    """
    Returns a set with all players in the fight
    """

    return self.q.filter(
        Predicate.isPlayerAction()
    ).map(
        Predicate.getActorInfo()
    ).set()

  @property
  def hostile_action(self) -> Query:
    # Hostile NPCs & (some of) Their Actions
    return self.q.filter(
        Predicate.isCreatureAction()
    ).filter(
        Predicate.isActorHostile()
    ).map(
        (Predicate.getActor(), Predicate.getEvent())
    )

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
