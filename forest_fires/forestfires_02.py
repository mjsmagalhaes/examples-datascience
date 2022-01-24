import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap

from tensorflow.keras.optimizers import RMSprop, SGD
from keras.models import Sequential
from keras.layers import Dense

from sklearn.preprocessing import OneHotEncoder
from lib.analysis import Analysis


# cmap_light = ListedColormap(["orange", "cornflowerblue"])
cmap_light = "Purples"
cmap_bold = ["white", "purple"]

raw = pd.read_csv("data/forestfires.csv")
a = Analysis(raw)

def categorise(x):
    if x == 0:
        return 'No Fire'
    # elif x < 100:
    #     return 'Small Fire'
    else:
        return 'Big Fire'

x = a.columns(['FFMC', 'DMC', 'DC', 'ISI', 'temp' , 'RH', 'wind', 'rain']).to_numpy()
# y = np.log(a.columns('area').to_numpy()+1)
# a.columns('area').plot.line()
y_cat = a.columns('area').apply(categorise)
# y_cat = y_cat.to_numpy().reshape(-1,1)
lb = OneHotEncoder()
y = lb.fit_transform(y_cat.to_numpy().reshape(-1,1)).toarray()

model = Sequential([
    Dense(units=5,activation='relu',input_shape=(8,)),
    Dense(units=2,activation='softmax')
])

model.summary()

model.compile(
    # optimizer=RMSprop(),
    optimizer=SGD(momentum=0.2,learning_rate=0.2),
    loss="mean_squared_error"
)

th = model.fit(
    x, y,
    epochs=3000, steps_per_epoch=1,
    validation_split=None, verbose=0
)

pd.DataFrame(th.history.get('loss'), columns=['loss']).plot.line()
y_pred = model.predict(x).round()
y_pred_cat = lb.inverse_transform(y_pred)

# Z = pd.DataFrame(Z,columns=['False', 'True'])
# y_pred = Z.idxmax(axis=1)
# y_true = a.columns('area').apply(lambda x: 'False' if x == 0 else 'True')

a.evaluate(y_cat, y_pred_cat )

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