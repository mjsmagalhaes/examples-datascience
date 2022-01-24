import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer, word_tokenize

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report

import dslib.nlp as nlp
from dslib.analysis import Analysis

# https://www.kaggle.com/bulentsiyah/nlp-basics-nltk-skipgram-cbow-reg-exp-stemmer/notebook#Content

sws = set(stopwords.words('english')).union({'.', ',', '...'})

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
tok = WhitespaceTokenizer()
cv = CountVectorizer()

raw = pd.read_csv('data/Restaurant_Reviews.csv')
lab = Analysis(raw)

data = list(map(lambda x: nlp.transform(
    x, sws, lambda x: ps.stem(x), word_tokenize), lab.columns('Review')))

y = lab.columns('Liked')
x = cv.fit_transform(data, y).toarray()

plt.figure(figsize=(15, 7))
sns.countplot(y)
plt.title("Liked")


x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.20, random_state=0)

gnb = GaussianNB()
gnb.fit(x_train, y_train)
y_pred = gnb.predict(x_test)

cm = confusion_matrix(y_test, y_pred, normalize="pred")
print("score: ", gnb.score(x_test, y_test))
print(classification_report(y_test, y_pred))

f, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(cm, annot=True, linewidths=0.5, linecolor="red", fmt=".2f", ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()
