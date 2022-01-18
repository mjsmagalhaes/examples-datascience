import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report
from .nlp import nlp

class Analysis:
    def __init__(self, data):
        self.data = data
        self.nlp = nlp()

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.data.to_string()

    # --- Information ---
    @staticmethod
    def from_csv(file):
        return Analysis(pd.read_csv(file))

    # --- Information ---
    @property
    def n_samples(self):
        return self.data.shape[0]

    @property
    def n_atributes(self):
        return self.data.shape[1]

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
    # --- PreProcess ---
    # --- Transform ---
    # --- Store ---
    # --- Evaluate ---
    def evaluate(self, y, y_pred, plot_cm=True, print_report=True):
        cm=confusion_matrix(y, y_pred)

        if plot_cm:
            f, ax = plt.subplots()
            sns.heatmap(
                cm,annot = True,
                linewidths=0.5,
                linecolor="red",
                fmt = ".2f",
                ax=ax
            )
            plt.xlabel("y_pred")
            plt.ylabel("y_true")
            plt.show()

        if print_report:
            print(classification_report(y, y_pred))

        return cm
