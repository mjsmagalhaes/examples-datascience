import spacy
import re
import pandas as pd

from functools import reduce

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer

class nlp:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

        self.sws = set(self.nlp.Defaults.stop_words)
        self.sws.update([
            ' ', ''
        ])

        self.vocabs = None

    def extract_vocab(self, corpus):
        self.vocabs = self.vocabs or set()

        def process(doc):
            sentence = re.sub('[^a-z]', ' ', doc.lower())
            tokens = self.nlp(sentence)
            lemma_list = map(lambda x: x.lemma_.strip().lower(), tokens)
            new_vocabs = [l for l in lemma_list if l not in self.sws]
            return new_vocabs

        def update(db, doc):
            db.update(doc)
            return db

        # Map + Reduce: Map doc to its vocabs and Reduce to set of vocabs.
        self.vocabs = set(reduce(
            update,
            map(lambda doc: process(doc), corpus),
            self.vocabs
        ))

        return self.vocabs


    def extract_corpus(self, corpus, vocabs=None):
        vocabs = vocabs or self.vocabs

        extracted_corpus = []
        for doc in corpus:
            sentence = re.sub('[^a-z]', ' ', doc.lower())
            tokens = self.nlp(sentence)
            lemma_list = list(map(lambda x: x.lemma_.strip().lower(), tokens))
            extracted_corpus.append(' '.join([l for l in lemma_list if l in vocabs]))

        return extracted_corpus

    def vectorize(self, extracted_corpus, vocabs=None):
        vec = CountVectorizer(vocabulary=vocabs)
        # vec.inverse_transform(M)
        return vec.transform(extracted_corpus).toarray()

if __name__ == '__main__':
    corpus = ['I like this car.', 'It has GPS navigation.', 'It price also very cheap']

    n = nlp()
    v = n.extract_vocab(corpus)

    # %% Old Code


    def parse_file(f):
        with open(f,'r') as data:
            corona_data = [text for text in data if text.count(' ') >= 2]

        return corona_data

    def transform(document, sws, lemma, tok):
        candidates = list(tok(document.lower()))
        # withMeaning = set(candidates).difference(sws).difference({'.',','})
        withMeaning = list(filter(lambda x: not (x in sws), candidates))
        # return list(map(lemma, withMeaning)), withMeaning, candidates
        return ' '.join(map(lemma, withMeaning))

    def vectorize_nltk(corpus):
        sws=set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        tokens = set()
        for document in corpus:
            final = self.transform(document)
            tokens.update(final)

        return tokens



    def vectorize(corpus,vocab=None):
        vectorizer=CountVectorizer(stop_words='english',vocabulary=vocab)
        M = vectorizer.fit_transform(corpus)

        m = pd.DataFrame(M.toarray(), columns = vectorizer.get_feature_names_out())
        print(m)

        return M, vectorizer