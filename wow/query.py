import pandas as pd
import datatable as dt


class Query:
  def __init__(self, data, inPlace=True):
    # print('New Query')
    self.data = data

  def __iter__(self):
    return self.iter()

  def iter(self):
    return iter(self.data)

  def apply(self, fn1, fn2, data):
    return Query(fn1(fn2, data))

  def map(self, fn):
    if type(fn) in [list, tuple]:

      def new_fn(x):
        return tuple(map(lambda f: f(x), fn))

      return self.apply(map, new_fn, self.iter())
    else:
      return self.apply(map, fn, self.iter())

  def filter(self, fn):
    return self.apply(filter, fn, self.iter())

  # --- Finalizers ---

  def set(self):
    return set(self.iter())

  def list(self):
    return list(self.iter())

  def tuple(self):
    return tuple(self.iter())

  def pandas(self, columns=None):
    return pd.DataFrame(self.iter(), columns=columns)

  def datatable(self, columns=None):
    return dt.Frame(self.pandas(columns=columns))


class Predicate:

  @staticmethod
  def isTarget(target):
    return lambda x: x['target'] == target

  @staticmethod
  def isActor(actor):
    return lambda x: x['actor'] == actor

  @staticmethod
  def isActorHostile():
    return lambda x: x.actor_mask.hostile == True

  # --- Actions ---

  @staticmethod
  def isAction(action):
    return lambda x: x['action'] == action

  @staticmethod
  def isPlayerAction():
    return lambda x: x['actor_tag'] == 'Player' and x['actor'] != '0'

  @staticmethod
  def isCreatureAction():
    return lambda x: x['actor_tag'] == 'Creature'

  # --- Events ---
  @staticmethod
  def isEvent(type):
    return lambda x: x.event == type

  @classmethod
  def isEncounterStart(cls):
    return cls.isEvent('ENCOUNTER_START')

  @classmethod
  def isEncounterEnd(cls):
    return cls.isEvent('ENCOUNTER_END')

  # --- Helpers ---
  @staticmethod
  def isActionCompound():
    return lambda r: type(r['action_e1']) == list

  # --- Getters ---

  def getData():
    return lambda x: x.rawdata

  def getEvent():
    return lambda x: x.event

  def getTimestamp():
    return lambda x: x.timestamp

  # --- Getters: Actor ---

  def getActor():
    return lambda x: x['actor']

  def getActorTag():
    return lambda x: x['actor_tag']

  def getActorId():
    return lambda x: x['actor_id']

  def getActorFlags():
    return lambda x: x['actor_flags']

  @classmethod
  def getActorInfo(cls):
    return (
        cls.getActor(),
        cls.getActorTag(),
        cls.getActorId()
    )

  # --- Getters: Target ---

  def getTarget():
    return lambda x: x['target']

  def getTargetTag():
    return lambda x: x['target_tag']

  def getTargetId():
    return lambda x: x['target_id']

  def getTargetFlags():
    return lambda x: x['target_flags']

  @classmethod
  def getTargetInfo(cls):
    return (
        cls.getTarget(),
        cls.getTargetTag(),
        cls.getTargetId()
    )

  # --- Getters: Actions ---

  def getAction():
    return lambda x: x['action']
