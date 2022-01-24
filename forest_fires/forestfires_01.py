import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

from lib.analysis import Analysis


cmap_light = ListedColormap(["orange", "cornflowerblue"])
cmap_bold = ["darkorange", "darkblue"]

data = pd.read_csv("data/forestfires.csv")
a = Analysis(data)

data = a.columns(['temp' , 'RH'])
category = a.columns('area').apply(lambda x: x != 0)

clf = KNeighborsClassifier(15)
clf.fit(data, category)

xx, yy = a.mesh(['temp', 'RH'])
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])


Z = Z.reshape(xx.shape)
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, cmap=cmap_light)


# Plot also the training points
sns.scatterplot(
    x=data['temp'],
    y=data['RH'],
    hue=category,
    palette=cmap_bold,
    alpha=1.0,
    edgecolor="black",
)

plt.title(
    "3-Class classification (k = %i, weights = '%s')" % (n_neighbors, weights)
)

plt.ylim(yy.min(), yy.max())
plt.xlim(xx.min(), xx.max())

plt.xlabel('temp')
plt.ylabel('RH')

plt.show()