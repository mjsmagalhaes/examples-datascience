import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap

from tensorflow.keras.optimizers import RMSprop, SGD
from keras.models import Sequential
from keras.layers import Dense

from sklearn.preprocessing import OneHotEncoder

from functools import partial


# cmap_light = ListedColormap(["orange", "cornflowerblue"])
cmap_light = "Purples"
cmap_bold = ["white", "purple"]


def categorise(boundaries, labels, x):
  f = pd.cut(x, boundaries, labels=labels)
  enc = OneHotEncoder()
  y = enc.fit_transform(f.to_numpy().reshape(-1, 1))
  return pd.DataFrame(y.todense(), columns=enc.categories_), f


# def build_sets(data: pd.DataFrame, boundary=0):
#   categorise = partial(proto_categorise, boundary)

#   x = data.drop(['area'], axis='columns')
#   y_cat = data.area.apply(categorise)

#   lb = OneHotEncoder()
#   y = lb.fit_transform(y_cat.to_numpy().reshape(-1, 1))

#   return x, pd.DataFrame(y.todense(), columns=lb.categories_)


def build_model(x: pd.DataFrame, y: pd.DataFrame):
  model = Sequential([
      Dense(units=50, activation='relu', input_shape=(8,)),
      Dense(units=2, activation='softmax')
  ])

  model.summary()

  model.compile(
      # optimizer=RMSprop(),
      optimizer=SGD(momentum=0.2, learning_rate=0.2),
      loss="mean_squared_error"
  )

  th = model.fit(
      x, y,
      epochs=30, steps_per_epoch=1,
      validation_split=None, verbose=0
  )

  pd.DataFrame(th.history.get('loss'), columns=['loss']).plot.line()

  return model, th

  # y_pred = model.predict(x)

  # y_pred_cat = lb.inverse_transform(y_pred)

  # Z = pd.DataFrame(Z,columns=['False', 'True'])
  # y_pred = Z.idxmax(axis=1)
  # y_true = a.columns('area').apply(lambda x: 'False' if x == 0 else 'True')

  # a.evaluate(y_cat, y_pred_cat)

  # xx, yy = a.mesh(['temp', 'RH'])
  # Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  # Z = pd.DataFrame(Z,columns=['False', 'True'])

  # Zsq = Z['True'].to_numpy().reshape(xx.shape)
  # plt.figure(figsize=(8, 6))
  # plt.contourf(xx, yy, Zsq, cmap=cmap_light)

  # data2 = a.columns(['temp' , 'RH'])
  # category2 = a.columns('area').apply(lambda x: 0 if x == 0 else 1)

  # # Plot also the training points
  # sns.scatterplot(
  #     x=data2['temp'],
  #     y=data2['RH'],
  #     hue=category2,
  #     palette=cmap_bold,
  #     alpha=1.0,
  #     edgecolor="black",
  # )

  # plt.ylim(yy.min(), yy.max())
  # plt.xlim(xx.min(), xx.max())

  # plt.xlabel('temp')
  # plt.ylabel('RH')

  # plt.show()
