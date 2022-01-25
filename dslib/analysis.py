import datatable as dt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report
from sklearn import preprocessing

from fast_ml.model_development import train_valid_test_split, train_test_split

from IPython.display import Markdown as md

from .nlp import nlp
from .plot import Plot


class Analysis:
  def __init__(self, data):
    self.data = data
    self.nlp = nlp()
    self.eda = Plot()

  def __repr__(self):
    return self.data

  def __str__(self):
    return self.data.to_string()

  # --- Factory ---
  @staticmethod
  def from_csv(file):
    raw = dt.fread(file).to_pandas()
    return Analysis(raw), raw

  # --- Information ---
  @property
  def n_samples(self):
    return self.data.shape[0]

  @property
  def n_atributes(self):
    return self.data.shape[1]

  def describe(self):
    print(self.data.info())
    return self.data.describe()

  def missing_data(self, data):
    m = np.sum(data.isna(), axis=0) + np.sum(data.isnull(), axis=0)
    s = pd.DataFrame(m, columns=['NA or Null'])
    return md(s.to_markdown())

  # --- Selection ---
  def drop_columns(self, columns):
    return self.data.drop(columns, axis='columns')

  def columns(self, name):
    return self.data[name]

  def mesh(self, columns, h=0.5):
    if len(columns) != 2:
      raise Exception("Columns Len Should be 2")

    X = self.data[columns[0]]
    x_min, x_max = X.min() - 1, X.max() + 1
    Y = self.data[columns[1]]
    y_min, y_max = Y.min() - 1, Y.max() + 1

    return np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

  def get_sets():
    pass

  # --- PreProcess ---
  def scaler_fit(self, data: pd.DataFrame):
    self.scaler = preprocessing.StandardScaler().fit(data)

  def scale(self, data: pd.DataFrame):
    scData = self.scaler.transform(data)
    return pd.DataFrame(scData, columns=data.columns)

  # --- Transform ---
  # --- Store ---

  # --- Evaluate ---
  def evaluate(
      self,
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
