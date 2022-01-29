import pandas as pd
import ipywidgets as widgets

from IPython.display import display, clear_output

from wow.query import Predicate
from wow.log import Encounter


def ui(encounters):
  encDropdown = widgets.Dropdown(
      options=list(map(lambda enc: (
          str(enc[0] + 1) + ' ' + enc[1].title(), enc[0]), enumerate(encounters))),
      value=0,
      description='Encounter:',
  )

  encButton = widgets.Button(
      description='Go!',
      disabled=False,
      button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Click me',
      icon='check'  # (FontAwesome names without the `fa-` prefix)
  )

  out = widgets.Output()

  def update(x):
    with out:
      clear_output()
      run(encounters[encDropdown.value])

  encButton.on_click(update)

  return widgets.VBox([
      widgets.HBox([encDropdown, encButton]),
      out
  ])


def run(encounter: Encounter):
  encounter.md()
  (orbSpawned, orbDisposed) = orbs_lifecycle(encounter)
  orbs_carriers(orbDisposed)
  orbs_overview(orbSpawned, orbDisposed)


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
  orbSpawned = e.q.filter(
      Predicate.isEvent('SPELL_AURA_APPLIED')
  ).filter(
      Predicate.isAction('"Eternal Torment"')
  ).map(
      (
          Predicate.getTimestamp(),
          Predicate.getTargetId(),
      )
  ).pandas(['TimeStamp', 'ID'])

  return (orbSpawned, orbDisposed)


def orbs_carriers(orbDisposed):
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


def orbs_overview(orbSpawned, orbDisposed):
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


def orbs_bugs(orbDisposed):
  return orbDisposed.groupby('ID').agg('count').style.applymap(
      lambda x: [None, 'color: yellow'][x > 1])
