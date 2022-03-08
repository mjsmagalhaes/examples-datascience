import glob
import os.path as path
from pathlib import Path
from ruamel.yaml import YAML

DOIT_CONFIG = {
    'action_string_formatting': 'new'
}


def get_target(file):
    _, f = path.split(file)
    fn, _ = path.splitext(f)
    p = Path('../mjsmagalhaes.github.io/content/notebook', fn + '.html')
    return p.relative_to('.')


def print_task(task):
    if path.exists(task.targets[0]):
        with open(task.targets[0], 'r') as f:
            content = f.readlines()
    else:
        content = None

    yaml = YAML()

    with open(task.targets[0], 'w') as f:
        f.write('---\n')
        yaml.dump(task.meta, f)
        f.write('---\n')
        if content:
            f.write(content)


def task_export():
    """export notebooks to html"""
    notebook_list = glob.glob('*.ipynb')

    for file in notebook_list:
        yield {
            'name': file,
            'file_dep': [file],
            'targets': [get_target(file)],
            'actions': [(
                f'jupyter nbconvert --to html {file} '
                r'--output-dir ..\mjsmagalhaes.github.io\content\notebook\ '
                r'--HTMLExporter.theme=dark'
            )],
            # 'clean': True,
            'verbosity': 2,
            'meta': {
                'title': '...'
            }
        }


def task_test():
    "run pytest"
    return {
        'actions': ['python -m pytest --html=report.html tests/'],
        'verbosity': 2,
    }
