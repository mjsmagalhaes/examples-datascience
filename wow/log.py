import datetime as date

from IPython.display import Markdown as md

from .query import Query


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
    self.idx = log[0]
    self.timestamp, rawdata = log[1].split('  ')
    self.rawdata = rawdata.split(',')
    self.event = self.rawdata[0]

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

  def hex_to_binary(hex_number: str, num_digits: int = 64) -> str:
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

    self.log = log[beg.idx: end.idx]

  def __repr__(self) -> str:
    return self.text()

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
    """.format(len(self.log), **self.__dict__)

  def md(self):
    return md(self.text())

  @property
  def q(self):
    return Query(self.log)
