# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 14:57:35 2022

@author: PICHAU
"""
import numpy as np
import pandas as pd
import math

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import gradient_descent_v2 as gd

i = np.array([[0, 0],[1,0],[0,1],[1,1]])
# o = np.array([0, 0, 0, 1])
o = np.array([0, 1, 1, 0])

model = Sequential([
    Dense(3, activation='sigmoid', input_shape=(2,)),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=gd.SGD(
        momentum=0.2,
        learning_rate=0.2
    ),
    loss='mean_squared_error'
)

# model.summary()

th = model.fit(x=i, y=o, epochs=7000, verbose=0)

pd.DataFrame(th.history.get('loss'), columns=['loss']).plot.line()
y_pred = model.predict(i)

