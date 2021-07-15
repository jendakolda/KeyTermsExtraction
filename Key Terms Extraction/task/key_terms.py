# Write your code here
# import lxml

from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.tokenize import word_tokenize


class KeyTermsExtractor:
    """Program to extract keywords from a XML document"""

    def __init__(self, file=None):
        if file:
            self.file = file
        else:
            self.file = input('Specify file to evaluate and its path:\n')

    def parser(self):
        xmlfile = open(self.file, "r").read()
        soup = BeautifulSoup(xmlfile, 'xml')
        all_values = soup.find_all('value')
        for item in all_values:
            if item.get('name') == 'head':
                print(item.get_text() + ':')
            elif item.get('name') == 'text':
                five_word_tokens = FreqDist(word_tokenize(item.get_text().lower())).most_common(5)
                five_words = [five_word_tokens[i][0] for i, v in enumerate(five_word_tokens)]
                print(*five_words, '\n')
                # print(*word_tokens[:5], '\n')


if __name__ == '__main__':
    KeyTermsExtractor('news.xml').parser()
