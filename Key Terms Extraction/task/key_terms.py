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
        for tag in all_values:
            if tag.get('name') == 'head':
                print(tag.get_text() + ':')
            elif tag.get('name') == 'text':
                # orders all the lowercase tokens from most to least common
                freq_tokens = sorted(FreqDist(word_tokenize(tag.get_text().lower())).most_common(), reverse=True)
                sorted_tokens = {k: v for k, v in sorted(dict(freq_tokens).items(), key=lambda item: item[1], reverse=True)[:5]}
                print(*[k for k in sorted_tokens.keys()], '\n')


if __name__ == '__main__':
    KeyTermsExtractor('news.xml').parser()
