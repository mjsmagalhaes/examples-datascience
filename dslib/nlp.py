import spacy
import re
import pandas as pd

from functools import reduce

# from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer

vocabs = None
nlp = spacy.load('en_core_web_sm')
sws = set(nlp.Defaults.stop_words)
sws.update([
    ' ', ''
])


def extract_vocab(corpus: list[str]) -> set[str]:
    vocabulary = set()

    def process(doc: str) -> list[str]:
        sentence = re.sub('[^a-z]', ' ', doc.lower())
        tokens = nlp(sentence)
        lemma_list = map(lambda x: x.lemma_.strip().lower(), tokens)
        new_vocabs = [lemma for lemma in lemma_list if lemma not in sws]
        return new_vocabs

    def update(db: set, doc: list[str]) -> set[str]:
        db.update(doc)
        return db

    # Map + Reduce: Map doc to its vocabs and Reduce to set of vocabs.
    vocabulary = set(reduce(
        update,
        map(lambda doc: process(doc), corpus),
        vocabulary
    ))

    return vocabulary


def extract_corpus(corpus: list, vocabulary=None):
    extracted_corpus = []
    for doc in corpus:
        sentence = re.sub('[^a-z]', ' ', doc.lower())
        tokens = nlp(sentence)
        lemma_list = list(map(lambda x: x.lemma_.strip().lower(), tokens))
        extracted_corpus.append(
            ' '.join([lemma for lemma in lemma_list if lemma in vocabulary]))

    return extracted_corpus


def vectorize(extracted_corpus, vocabulary=None):
    vec = CountVectorizer(vocabulary=vocabulary)
    # vec.inverse_transform(M)
    return vec.transform(extracted_corpus).toarray()


if __name__ == '__main__':
    example_corpus = [
        'I like this car.',
        'It has GPS navigation.',
        'It price also very cheap'
    ]

    vocabulary = extract_vocab(example_corpus)
    print('Vocabulary:', vocabulary)

    extracted_corpus = extract_corpus(example_corpus, vocabulary)
    print('Corpus:', extracted_corpus)

    exit()

    # %% Old Code

    def parse_file(f):
        with open(f, 'r') as data:
            corona_data = [text for text in data if text.count(' ') >= 2]

        return corona_data

    def transform(document, sws, lemma, tok):
        candidates = list(tok(document.lower()))
        # withMeaning = set(candidates).difference(sws).difference({'.',','})
        withMeaning = list(filter(lambda x: not (x in sws), candidates))
        # return list(map(lemma, withMeaning)), withMeaning, candidates
        return ' '.join(map(lemma, withMeaning))

    def vectorize_nltk(corpus):
        sws = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        tokens = set()
        for document in corpus:
            final = transform(document)
            tokens.update(final)

        return tokens

    def vectorize(corpus, vocab=None):
        vectorizer = CountVectorizer(stop_words='english', vocabulary=vocab)
        M = vectorizer.fit_transform(corpus)

        m = pd.DataFrame(
            M.toarray(), columns=vectorizer.get_feature_names_out())
        print(m)

        return M, vectorizer
