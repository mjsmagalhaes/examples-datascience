import os
import click
import requests

from plyer import notification


def list_dir(dir='data', ext='.csv'):
    path = os.walk(dir)
    file_list = []
    for root, directories, files in path:
        # for directory in directories:
        #     print(directory)

        for file in files:
            _, fileExt = os.path.splitext(file)
            if fileExt == ext:
                file_list.append(os.path.join(root, file))

    return file_list

# notification.notify(
#     title="Sample Notification",
#     message="This is a sample notification",
#     timeout=10
# )


@click.group()
def cli():
    pass


@cli.command(name='list-dir')
@click.option('--dir', default='data', help='Directory to parse.')
@click.option('--ext',  default='.csv', help='File extension to match.')
def print_list_dir(dir, ext):
    print(list_dir(dir, ext))


@cli.command()
def upload():
    test_url = 'http://127.0.0.1:8000/upload/log'
    test_files = {
        "file": open("export.ps1", "r"),
    }

    test_response = requests.post(test_url, files=test_files)

    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print("Something went wrong!")


if __name__ == '__main__':
    cli()
