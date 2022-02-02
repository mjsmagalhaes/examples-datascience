import pandas as pd

# import ipywidgets as widgets

from IPython.display import display

from wow import ENCOUNTER_DATA
from wow.query import Predicate, Query
from wow.log import EncounterReport


class NerzhulReport(EncounterReport):
  def report(self):
    self.showEncounters()
    (orbSpawned, orbDisposed) = self.getOrbInfo()
    self.showOrbCarriers(orbDisposed)
    self.showOrbLifecycle(orbSpawned, orbDisposed)

  def listOrbsSpawned(self) -> Query:
    """
    Finds when orbs are spawned
    """

    return self.q.filter(
        Predicate.isEvent('SPELL_AURA_APPLIED')
    ).filter(
        Predicate.isAction('"Eternal Torment"')
    ).map(
        (
            Predicate.getTimestamp(),
            Predicate.getTargetId(),
        )
    )

  def listOrbsDisposed(self) -> Query:
    """
    Finds when orbs are picked up
    """

    return self.q.filter(
        Predicate.isEvent('SPELL_AURA_APPLIED')
    ).filter(
        Predicate.isAction('"Sorrowful Procession"')
    ).map(
        (
            Predicate.getTimestamp(),
            Predicate.getActorId(),
            Predicate.getTarget()
        )
    )

  def getOrbInfo(self):
    """ Find when orbs spawn and die. """

    orbDisposed = self.listOrbsDisposed().pandas(
        ['TimeStamp', 'ID', 'Player']
    )

    # When Orbs Spawn
    orbSpawned = self.listOrbsSpawned().pandas(
        ['TimeStamp', 'ID']
    )

    return (orbSpawned, orbDisposed)

  def showOrbCarriers(self, orbDisposed: pd.DataFrame):
    """ Creates a list of orb carriers. """

    idx = orbDisposed.sort_values('ID').duplicated(subset='ID', keep=False)

    tableCarriers = orbDisposed.sort_values('ID').style.applymap(
        lambda x: 'color: blue; font-weight: bold', subset=pd.IndexSlice[idx, :]
    ).set_caption('List of Orb Carriers').set_table_styles([{
        'selector': 'caption',
        'props': [
            ('font-size', '16px'),
            ('font-weight', 'bold')
        ]
    }])

    display(tableCarriers)

    return tableCarriers

  def showOrbLifecycle(self, orbSpawned: pd.DataFrame, orbDisposed: pd.DataFrame):
    """ Creates a table with orb data. """

    orbsData = pd.merge(
        orbSpawned,
        pd.merge(
            orbDisposed.groupby('ID')['TimeStamp'].max(),
            orbDisposed,
            on='TimeStamp',
            how='inner'
        ),
        on='ID',
        how='inner'
    )

    # orbsData['TimeStamp_x'] = pd.to_datetime(
    #     orbsData['TimeStamp_x'])

    # orbsData['TimeStamp_y'] = pd.to_datetime(
    #     orbsData['TimeStamp_y'], format="%m/%d %H:%M:%S.%f")

    table = pd.merge(
        orbsData,
        pd.DataFrame(orbsData['TimeStamp_y'] -
                     orbsData['TimeStamp_x'], columns=['Time Elapsed']),
        on=orbsData.index
    )[['ID', 'TimeStamp_x', 'TimeStamp_y', 'Time Elapsed', 'Player']]

    table.columns = [
        'ID',
        'TimeStamp Spawned', 'TimeStamp Disposed', 'Time Elapsed',
        'Player'
    ]

    tableOverview = table.style.applymap(
        lambda x: 'color: blue; font-weight: bold', subset=pd.IndexSlice[:, ['Time Elapsed']]
    ).applymap(
        lambda x: 'color: aqua', subset=pd.IndexSlice[:, ['TimeStamp Spawned', 'TimeStamp Disposed']]
    ).set_caption('Orb Lifespan Overview').set_table_styles([{
        'selector': 'caption',
        'props': [
            ('font-size', '16px'),
            ('font-weight', 'bold')
        ]
    }])

    display(tableOverview)

    return tableOverview

  def orbs_bugs(self, orbDisposed: pd.DataFrame):
    return orbDisposed.groupby('ID').agg('count').style.applymap(
        lambda x: [None, 'color: yellow'][x > 1])


ENCOUNTER_DATA[2432] = NerzhulReport
