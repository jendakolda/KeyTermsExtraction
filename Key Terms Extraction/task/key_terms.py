# Write your code here
# import lxml

from bs4 import BeautifulSoup
from collections import Counter
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
        for tag in all_values:
            if tag.get('name') == 'head':
                print(tag.get_text() + ':')
            elif tag.get('name') == 'text':
                word_list = word_tokenize(tag.get_text().lower())
                counted_dict = Counter(sorted(word_list, reverse=True))
                print(*[x[0] for x in counted_dict.most_common(5)])



if __name__ == '__main__':
    KeyTermsExtractor('news.xml').parser()
