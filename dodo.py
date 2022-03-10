import glob
import os.path as path
from doit import task_params
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
    notebook_list = glob.glob('dsexamples/*.ipynb')

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
        'actions': ['python -m pytest --html=tests/report.html tests/'],
        'verbosity': 2,
    }


@task_params([
    {'name': 'build', 'long': 'build', 'type': bool, 'default': False},
    {'name': 'clear', 'long': 'prune', 'type': bool, 'default': False},
])
def task_docker(build, clear):
    if build:
        yield {
            'name': 'docker-build',
            'actions': ['docker build --tag dslib .'],
            'verbosity': 2
        }

    if clear:
        yield {
            'name': 'docker-clear',
            'actions': [
                'echo - Removing Unused Docker Volumes:',
                'docker volume prune -f',
                'echo - Removing Unused Docker Containers:',
                'docker container prune -f',
                'echo - Removing Unused Docker Images:',
                'docker container prune -f'
            ],
            'verbosity': 2
        }


def task_publish():
    """push to keroku"""
    return {
        'actions': ['git push heroku main']
    }


def task_local():
    return {
        'actions': ['heroku local -f .\Procfile.windows'],
        'verbosity': 2,
    }


# 'heroku stack:set container'
# 'npx parcel serve --public-url /wordcloud/assets'
# 'python -m build'

'docker run -it --name backend dslib:backend'
'docker commit backend dslib:backend'

'docker run -it --name frontend dslib:frontend'
'docker commit frontend dslib:frontend'

'docker build --tag dslib .'
