import datetime as date

from .query import Query


class Mask():
  def __init__(self, flags):
    self.flags = flags

  @property
  def hostile(self):
    return self.flags[6] == '1'


class Record:
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
      self.actor_id, self.actor = self.rawdata[1:3]
      self.actor_flags = bin(int(self.rawdata[3], 16))[2:].zfill(64)[::-1]
      # self.actor_marks = bin(int(self.rawdata[4], 16))[2:].zfill(64)[::-1]
      self.actor_tag, *_ = self.actor_id.split('-')

      self.target_id, self.target = self.rawdata[5:7]
      self.target_flags = bin(int(self.rawdata[7], 16))[2:].zfill(64)[::-1]
      # self.target_marks = bin(int(self.rawdata[8], 16))[2:].zfill(64)[::-1]
      self.target_tag, *_ = self.target_id.split('-')
    else:
      try:
        self.actor_id, self.actor = self.rawdata[1:3]
        self.actor_flags = bin(int(self.rawdata[3], 16))[2:].zfill(64)[::-1]
        # self.actor_marks = bin(int(self.rawdata[4], 16))[2:].zfill(64)[::-1]
        self.actor_tag, *_ = self.actor_id.split('-')

        self.target_id, self.target = self.rawdata[5:7]
        self.target_flags = bin(int(self.rawdata[7], 16))[2:].zfill(64)[::-1]
        # self.target_marks = bin(int(self.rawdata[8], 16))[2:].zfill(64)[::-1]
        self.target_tag, *_ = self.target_id.split('-')

        self.action_id, self.action, *self.action_e1 = self.rawdata[9:]
      except:
        print(log)
        raise Exception('BOOM.')

  def __str__(self) -> str:
    return '{date}: {event}'.format(**self.__dict__)

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
  def actor_mask(self):
    return Mask(self.actor_flags)

  def hex_to_binary(hex_number: str, num_digits: int = 32) -> str:
    """
    Converts a hexadecimal value into a string representation
    of the corresponding binary value
    Args:
        hex_number: str hexadecimal value
        num_digits: integer value for length of binary value.
                    defaults to 8

    Returns:
        string representation of a binary number 0-padded
        to a minimum length of <num_digits>
    """
    return str(bin(int(hex_number, 16)))[2:].zfill(num_digits)


class Encounter:
  def __init__(self, log, beg, end):
    self.beg = beg
    self.timestamp_begin = date.datetime.strptime(
        beg.timestamp, '%m/%d %H:%M:%S.%f')
    self.end = end
    self.timestamp_end = date.datetime.strptime(
        end.timestamp, '%m/%d %H:%M:%S.%f')
    self.log = log[beg.idx: end.idx]

  def __repr__(self) -> str:
    return """
    {timestamp_begin}
    {beg.event} Log[{beg.idx}]
    {0} entries
    {end.event} Log[{end.idx}]
    {timestamp_end}
    """.format(len(self.log), **self.__dict__)

  @property
  def q(self):
    return Query(self.log)
