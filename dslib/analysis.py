from collections import namedtuple
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# from .nlp import nlp
# from .plots import Plot

Dataset = namedtuple('Dataset', 'x y')


# --- Information ---


def n_samples(data):
  return data.shape[0]


def n_atributes(data):
  return data.shape[1]


def describe(data):
  print(data.info())
  return data.describe()

# --- Selection ---


def drop_columns(data, columns):
  return data.drop(columns, axis='columns')


def columns(data, name):
  return data[name]


def mesh(data, columns, h=0.5):
  if len(columns) != 2:
    raise Exception("Columns Len Should be 2")

  X = data[columns[0]]
  x_min, x_max = X.min() - 1, X.max() + 1
  Y = data[columns[1]]
  y_min, y_max = Y.min() - 1, Y.max() + 1

  return np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# --- PreProcess ---


def scaler_fit(data: pd.DataFrame):
  return preprocessing.StandardScaler().fit(data)


def scale(data: pd.DataFrame, scaler):
  scData = scaler.transform(data)
  return pd.DataFrame(scData, columns=data.columns)

# --- Transform ---
# --- Store ---


def partition(x, y, n_test=0.4, n_validation=0):

  n_split = n_test + n_validation

  p = train_test_split(x, y, test_size=n_split)

  if n_validation == 0:
    Partition = namedtuple('Partition', 'train test')
    return Partition(
        Dataset(p[0], p[2]),  # train.x, train.y
        Dataset(p[1], p[3])  # test.x, test.y
    )
  else:
    Partition = namedtuple('Partition', 'train test valid')
    q = train_test_split(p[1], p[3], test_size=n_validation / n_split)
    return Partition(
        Dataset(p[0], p[2]),  # train.x, train.y
        Dataset(q[0], q[2]),  # test.x, test.y
        Dataset(q[1], q[3]),  # valid.x, valid.y
    )

# --- Evaluate ---


def evaluate(
    y, y_pred,
    plot_cm=True, print_report=True, title='Evaluation'
):
  cm = confusion_matrix(y, y_pred)

  if plot_cm:
    f, ax = plt.subplots()
    sns.heatmap(
        cm,
        annot=True,
        linewidths=0.5,
        linecolor="red",
        fmt=".2f",
        ax=ax
    )
    plt.title(title)
    plt.xlabel("y_pred")
    plt.ylabel("y_true")
    plt.show()

  if print_report:
    print(classification_report(y, y_pred))

  return cm
