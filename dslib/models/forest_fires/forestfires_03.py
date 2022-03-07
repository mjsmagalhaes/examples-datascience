# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:18:34 2022

@author: PICHAU
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.neural_network import MLPRegressor

from lib.analysis import Analysis

raw = pd.read_csv("data/forestfires.csv")
lab = Analysis(raw)

x = lab.columns(['FFMC', 'DMC', 'DC', 'ISI', 'temp' , 'RH', 'wind']).to_numpy()
y = np.log(lab.columns('area').to_numpy()+1)

nn = MLPRegressor(
        solver='sgd',
        activation='logistic',
        hidden_layer_sizes=(7),
        # learning_rate='invscaling',
        learning_rate_init=0.001,
        momentum=0.9,
        # power_t=0.1,
        max_iter=10000,
        # early_stopping = True,
        random_state = 1001
    )

model = nn.fit(x,y)
y_pred = nn.predict(x)
print(abs(y - y_pred).mean())

c = pd.DataFrame(model.loss_curve_)
c.plot.line()
# e = pd.DataFrame(abs(y - y_pred))
# e.plot.line()
print(model.score(x, y_pred))
