# Write your code here
import string

from bs4 import BeautifulSoup
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class KeyTermsExtractor:
    """Program to extract keywords from a XML document"""

    def __init__(self, file=None):
        if file:
            self.file = file
        else:
            self.file = input('Specify file to evaluate and its path:\n')
        self.sw = stopwords.words('english')
        self.punctuation = list(string.punctuation)

    def clean_list(self, words: list):
        return [word for word in words if (word not in self.sw) and (word not in self.punctuation)]

    def tokenizer(self, text, n_most_freq=5):
        word_list = word_tokenize(text.lower())
        word_list = self.clean_list(word_list)
        word_list = self.lemmatizer(word_list)
        counted_dict = Counter(sorted(word_list, reverse=True))
        return [x[0] for x in counted_dict.most_common(n_most_freq)]

    def lemmatizer(self, words):
        wnl = WordNetLemmatizer()
        lemmatized = list()
        for word in words:
            lemmatized.append(wnl.lemmatize(word))
        return lemmatized

    def parser(self):
        xmlfile = open(self.file, "r").read()
        soup = BeautifulSoup(xmlfile, 'xml')
        all_values = soup.find_all('value')
        for tag in all_values:
            if tag.get('name') == 'head':
                print(tag.get_text() + ':')
            elif tag.get('name') == 'text':
                five_most_common = self.tokenizer(tag.get_text())
                print(*five_most_common, '\n')


if __name__ == '__main__':
    KeyTermsExtractor('news.xml').parser()
