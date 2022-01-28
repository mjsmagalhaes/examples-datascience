import pandas as pd
from wow.query import Predicate
from wow.log import Encounter


def orbs_lifecycle(e: Encounter):
  """ Find when orbs spawn and die. """

  # When Orbs 'Die'
  orbDisposed = e.q.filter(
      Predicate.isEvent('SPELL_AURA_APPLIED')
  ).filter(
      Predicate.isAction('"Sorrowful Procession"')
  ).map(
      (
          Predicate.getTimestamp(),
          Predicate.getActorId(),
          Predicate.getTarget()
      )
  ).pandas(['TimeStamp', 'ID', 'Player'])

  # When Orbs Spawn
  orbBorn = e.q.filter(
      Predicate.isEvent('SPELL_AURA_APPLIED')
  ).filter(
      Predicate.isAction('"Eternal Torment"')
  ).map(
      (
          Predicate.getTimestamp(),
          Predicate.getTargetId(),
      )
  ).pandas(['TimeStamp', 'ID'])

  return (orbBorn, orbDisposed)


def orbs_carriers(orbDisposed):
  idx = orbDisposed.sort_values('ID').duplicated(subset='ID', keep=False)
  return orbDisposed.sort_values('ID').style.applymap(
      lambda x: 'color: yellow', subset=pd.IndexSlice[idx, :]
  )


def orbs_overview(orbBorn, orbDisposed):
  orbsData = pd.merge(
      orbBorn,
      pd.merge(
          orbDisposed.groupby('ID')['TimeStamp'].max(),
          orbDisposed,
          on='TimeStamp',
          how='inner'
      ),
      on='ID',
      how='inner'
  )

  orbsData['TimeStamp_x'] = pd.to_datetime(
      orbsData['TimeStamp_x'], format="%m/%d %H:%M:%S.%f")

  orbsData['TimeStamp_y'] = pd.to_datetime(
      orbsData['TimeStamp_y'], format="%m/%d %H:%M:%S.%f")

  table = pd.merge(
      orbsData,
      pd.DataFrame(orbsData['TimeStamp_y'] -
                   orbsData['TimeStamp_x'], columns=['Time Elapsed']),
      on=orbsData.index
  )[['ID', 'TimeStamp_x', 'TimeStamp_y', 'Time Elapsed', 'Player']]

  return table.style.applymap(
      lambda x: 'color: yellow', subset=pd.IndexSlice[:, ['Time Elapsed']]
  ).applymap(
      lambda x: 'color: aqua', subset=pd.IndexSlice[:, ['TimeStamp_x', 'TimeStamp_y']]
  )


def orbs_bugs(orbDisposed):
  return orbDisposed.groupby('ID').agg('count').style.applymap(
      lambda x: [None, 'color: yellow'][x > 1])
