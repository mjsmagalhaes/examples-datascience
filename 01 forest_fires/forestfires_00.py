
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

from lib.analysis import Analysis


if __name__ == "__main__":
    data = pd.read_csv("data/forestfires.csv")
    a = Analysis(data)
    print(a.data)
    
    a.columns('area').plot(kind='line')
    a.data['has_fire'] = a.data['area'].apply(lambda x: x != 0)
    a.data['has_fire'].value_counts().plot.bar()
    
    data = a.columns(['temp' , 'RH', 'wind', 'rain'])
    category = a.columns('has_fire')
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(data, category)
    p = knn.predict(data)
    
    results = pd.DataFrame(list(map(lambda x, y: x==y, p, category)))
    print(results.value_counts())
    
    print(classification_report(category, p))
    cm = confusion_matrix(category, p)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    
    
    
    # fig, ax = plt.subplots()
    # ax.plot(results)
    # ax.legend()
    # plt.show()