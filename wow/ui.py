import ipywidgets as widgets
from zipfile import ZipFile

from IPython.display import display, clear_output

from wow.fights import nerzhul


def import_file():
  zipText = widgets.Text()
  zipBtn = widgets.Button(
      description='Unzip',
      disabled=False,
      button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Click me',
      icon='check'  # (FontAwesome names without the `fa-` prefix)
  )

  fileText = widgets.Text()
  fileBtn = widgets.Button(
      description='Load',
      disabled=False,
      button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
      tooltip='Click me',
      icon='check'  # (FontAwesome names without the `fa-` prefix)
  )

  def load(x):
    with open(fileText.value, 'r', encoding='utf-8') as filePtr:
      fileText.content = filePtr.readlines()

  def unzip(x):
    with ZipFile(zipText.value) as f:
      f.extractall('wow_data')

  fileBtn.on_click(load)
  zipBtn.on_click(unzip)

  display(
      widgets.VBox([
          widgets.HBox([
              zipText,
              zipBtn
          ]),
          widgets.HBox([
              fileText,
              fileBtn
          ])
      ])
  )

  return (zipText, fileText)


def pick_encounter(encounters):
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
      nerzhul.run(encounters[encDropdown.value])

  encButton.on_click(update)

  display(
      widgets.VBox([
          widgets.HBox([encDropdown, encButton]),
          out
      ])
  )

  return encDropdown
