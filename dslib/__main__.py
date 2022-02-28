import os


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


if __name__ == '__main__':
  print(list_dir())
