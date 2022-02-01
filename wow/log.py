from __future__ import annotations

import datetime as date

from IPython.display import display, Markdown as md
from itertools import islice
from more_itertools import ilen
from typing import List, Set, Tuple

from .query import Query, Predicate


class Mask():
  def __init__(self, flags):
    self.flags = flags

  @property
  def hostile(self):
    return self.flags[6] == '1'


class Record:
  """
  Represents a line in the log file.
  """

  def __init__(self, log: str):
    try:
      self.idx = log[0]
      self.timestamp, rawdata = log[1].split('  ')
      self.rawdata = rawdata.split(',')
      self.event = self.rawdata[0]
    except:
      print(log)
      raise Exception('BOOM.')

    if(self.event in [
        'COMBAT_LOG_VERSION', 'ZONE_CHANGE', 'MAP_CHANGE',
        'PARTY_KILL',
        'ENCOUNTER_START', 'ENCOUNTER_END',
        'WORLD_MARKER_PLACED', 'WORLD_MARKER_REMOVED',
        'EMOTE'
    ]):
      return
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
      return self.rawdata[idx]
    else:
      return None

  @property
  def actor_mask(self) -> Mask:
    return Mask(self.actor_flags)

  def parse_actor(self):
    self.actor_id, self.actor = self.rawdata[1:3]
    self.actor_flags = self.hex_to_binary(self.rawdata[3])
    # self.actor_marks = bin(int(self.rawdata[4], 16))[2:].zfill(64)[::-1]
    self.actor_tag, *_ = self.actor_id.split('-')

  def parse_target(self):
    self.target_id, self.target = self.rawdata[5:7]
    self.target_flags = self.hex_to_binary(self.rawdata[7])
    # self.target_marks = bin(int(self.rawdata[8], 16))[2:].zfill(64)[::-1]
    self.target_tag, *_ = self.target_id.split('-')

  def parse_action(self):
    self.action_id, self.action, *self.action_e1 = self.rawdata[9:]

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


class Encounter:
  """
  Represents a group of Records in a single Encounter.

  A encounter starts with the event ENCOUNTER_START and finishes with a ENCOUNTER_END event.
  """

  @staticmethod
  def parse(logLines) -> List[Encounter]:
    # Create Record List
    log = Query(enumerate(logLines)).map(lambda x: Record(x)).list()

    # Split Encounters

    qLog = Query(log)
    beg = qLog.filter(Predicate.isEncounterStart())
    end = qLog.filter(Predicate.isEncounterEnd())

    encounters = Query(zip(beg, end)).map(
        lambda x: Encounter(log, x[0], x[1])
    )

    e = encounters.filter(
        lambda x: x.duration.total_seconds() > 60
    ).list()
    print(len(encounters.list()), ' => ', len(e))

    return (log, e)

  def __init__(self, log, beg, end):
    self.beg = beg
    self.timestamp_begin = date.datetime.strptime(
        beg.timestamp, '%m/%d %H:%M:%S.%f'
    ).replace(year=2022)

    self.end = end
    self.timestamp_end = date.datetime.strptime(
        end.timestamp, '%m/%d %H:%M:%S.%f'
    ).replace(year=2022)

    self.duration = self.timestamp_end - self.timestamp_begin

    self.id = int(beg.rawdata[1])
    self.name = beg.rawdata[2]

    self.log = log

  def __repr__(self) -> str:
    return self.text()

  def __iter__(self):
    return self.iter

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
    """.format(ilen(self.iter), **self.__dict__)

  def md(self):
    display(md(self.text()))

  @property
  def q(self):
    return Query(self.iter)

  @property
  def iter(self):
    return islice(self.log, self.beg.idx, self.end.idx + 1)

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
