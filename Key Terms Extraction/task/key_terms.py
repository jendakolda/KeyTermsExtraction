# Write your code here
import string
from collections import Counter

from bs4 import BeautifulSoup
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class KeyTermsExtractor:
    """Program to extract keywords from a XML document"""
    sw = stopwords.words('english')
    punctuation = list(string.punctuation)
    headers = list()
    vocabulary = list()

    def __init__(self, file=None):
        if file:
            self.file = file
        else:
            self.file = input('Specify file to evaluate and its path:\n')

    @staticmethod
    def lemmatizer(words):
        wnl = WordNetLemmatizer()
        lemmatized = list()
        for word in words:
            lemmatized.append(wnl.lemmatize(word))
        return lemmatized

    @staticmethod
    def clean_list(words: list):
        return [word for word in words if (word not in KeyTermsExtractor.sw)
                and (word not in KeyTermsExtractor.punctuation)]

    @staticmethod
    def pos_sort(words, part_of_speech='NN'):
        return [word for word in words if pos_tag([word])[0][1] == part_of_speech]

    @staticmethod
    def create_tfidf_matrix(dataset):
        vectorizer = TfidfVectorizer(input='content', use_idf=True, lowercase=True,
                                     analyzer='word', ngram_range=(1, 1),
                                     stop_words=None)
        vect = vectorizer.fit_transform(dataset)
        names = vectorizer.get_feature_names()
        print(names)
        return vect, names

    def text_processor(self, text):
        word_list = word_tokenize(text.lower())  # Lists individual words
        word_list = self.lemmatizer(word_list)  # converts to a dictionary form of lemma
        word_list = self.clean_list(word_list)  # remove stop words and punctuation
        word_list = self.pos_sort(word_list)  # filters out only selected pos
        KeyTermsExtractor.vocabulary.append(' '.join(word_list))

    @staticmethod
    def pick_best_scoring(words, n_most_frequent=5):
        counted_dict = Counter(sorted(words, reverse=True))
        return [x[0] for x in counted_dict.most_common(n_most_frequent)]

    def xml_parser(self):
        xmlfile = open(self.file, "r").read()
        soup = BeautifulSoup(xmlfile, 'xml')
        all_values = soup.find_all('value')
        for tag in all_values:
            if tag.get('name') == 'head':
                KeyTermsExtractor.headers.append(tag.get_text() + ':')
            elif tag.get('name') == 'text':
                self.text_processor(tag.get_text())
                # print(*five_most_common, '\n')

        # if len(KeyTermsExtractor.headers) == len(KeyTermsExtractor.vocabulary):
        #     quit('non-matching lengths')

        matrix, feature_names = self.create_tfidf_matrix(KeyTermsExtractor.vocabulary)
        #
        print(matrix)
        print(feature_names)
        for i, header in enumerate(KeyTermsExtractor.headers):
            print(header)


if __name__ == '__main__':
    KeyTermsExtractor('news.xml').xml_parser()
