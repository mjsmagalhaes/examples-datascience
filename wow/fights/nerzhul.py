import pandas as pd

# import ipywidgets as widgets

from IPython.display import display
from more_itertools import ilen

from wow import ENCOUNTER_DATA
from wow.query import Predicate, Query
from wow.log import EncounterReport


class NerzhulReport(EncounterReport):
  def highlightStyle(self):
    return 'color: yellow; font-weight: bold'

  def report(self):
    # self.showEncounters()
    (orbSpawned, orbDisposed) = self.getOrbInfo()
    # self.showOrbCarriers(orbDisposed)
    return self.showOrbLifecycle(orbSpawned, orbDisposed)

  def listThrowCasts(self) -> Query:
    """
    Finds when orbs are spawned
    """

    return self.q.filter(
        Predicate.isEventIn(['SPELL_AURA_APPLIED'])
    ).filter(
        Predicate.isAction('"Sorrowful Procession"')
    ).map(
        (
            Predicate.getTimestamp(),
            Predicate.getTarget(),
        )
    ).groupby(
        lambda x: x[1], reducefn=ilen
    ).sort(
        lambda x: x[1],
        reverse=True
    )

  def listDebuffApplication(self) -> Query:
    """
    Finds when orbs are picked up
    """

    return self.q.filter(
        Predicate.all([
            Predicate.isEventIn(['SPELL_CAST_SUCCESS']),
            Predicate.isAction('"Throw"')
        ])
    ).map(
        (
            Predicate.getTimestamp(),
            Predicate.getActor(),
        )
    ).groupby(
        lambda x: x[1], reducefn=ilen
    ).sort(
        lambda x: x[1],
        reverse=True
    )

  def getOrbInfo(self):
    """ Find when orbs spawn and die. """

    # When Orbs Spawn
    orbSpawned = self.listThrowCasts().pandas(
        ['Player', 'Debuff Applied']
    )

    orbDisposed = self.listDebuffApplication().pandas(
        ['Player', 'Throw Casts']
    )

    return (orbSpawned, orbDisposed)

  def showOrbCarriers(self, orbDisposed: pd.DataFrame):
    """ Creates a list of orb carriers. """

    # idx = orbDisposed.sort_values('').duplicated(subset='ID', keep=False)

    # tableCarriers = orbDisposed.sort_values('ID').style.applymap(
    #     lambda x: self.highlightStyle(), subset=pd.IndexSlice[idx, :]
    # ).set_caption('List of Orb Carriers').set_table_styles([{
    #     'selector': 'caption',
    #     'props': [
    #         ('font-size', '16px'),
    #         ('font-weight', 'bold')
    #     ]
    # }])

    tableCarriers = orbDisposed

    display(tableCarriers)

    return tableCarriers

  def showOrbLifecycle(self, orbSpawned: pd.DataFrame, orbDisposed: pd.DataFrame):
    """ Creates a table with orb data. """

    # orbsData = pd.merge(
    #     orbSpawned,
    #     pd.merge(
    #         orbDisposed.groupby('ID')['TimeStamp'].max(),
    #         orbDisposed,
    #         on='Player',
    #         how='inner'
    #     ),
    #     on='ID',
    #     how='inner'
    # )

    # orbsData['TimeStamp_x'] = pd.to_datetime(
    #     orbsData['TimeStamp_x'])

    # orbsData['TimeStamp_y'] = pd.to_datetime(
    #     orbsData['TimeStamp_y'], format="%m/%d %H:%M:%S.%f")

    # table = pd.merge(
    #     orbsData,
    #     pd.DataFrame(orbsData['TimeStamp_y'] -
    #                  orbsData['TimeStamp_x'], columns=['Time Elapsed']),
    #     on=orbsData.index
    # )[['ID', 'TimeStamp_x', 'TimeStamp_y', 'Time Elapsed', 'Player']]

    table = pd.merge(
        orbSpawned,
        orbDisposed,
        on='Player'
    )

    # table.columns = [
    #     'ID',
    #     'TimeStamp Spawned', 'TimeStamp Disposed', 'Time Elapsed',
    #     'Player'
    # ]

    # tableOverview = table.style.applymap(
    #     lambda x: self.highlightStyle(), subset=pd.IndexSlice[:, ['Time Elapsed']]
    # ).applymap(
    #     lambda x: 'color: aqua', subset=pd.IndexSlice[:, ['TimeStamp Spawned', 'TimeStamp Disposed']]
    # ).set_caption('Orb Lifespan Overview').set_table_styles([{
    #     'selector': 'caption',
    #     'props': [
    #         ('font-size', '16px'),
    #         ('font-weight', 'bold')
    #     ]
    # }])

    table['%'] = table['Throw Casts'] * 100 / table['Debuff Applied']

    display(table)

    return table

  def orbs_bugs(self, orbDisposed: pd.DataFrame):
    return orbDisposed.groupby('ID').agg('count').style.applymap(
        lambda x: [None, 'color: yellow'][x > 1])


ENCOUNTER_DATA[2432] = NerzhulReport
