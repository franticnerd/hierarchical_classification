from nltk.corpus import stopwords
from nltk.stem.porter import *
import re

class TextParser:

    def __init__(self, min_length=3, stopword_file=None):
        self.min_length = min_length
        self.stopwords = set(stopwords.words('english'))
        if stopword_file is not None:
            self.load_stopwords(stopword_file)
        # print len(self.stopwords)

    '''
    Allow a user to specify stopwords through a file; each line is a stop word.
    '''
    def load_stopwords(self, stopword_file):
        with open(stopword_file, 'r') as fin:
            for line in fin:
                stopword = line.strip()
                self.stopwords.add(stopword)

    '''
    Parse a string into a list of words. Perform stemming and stopword removal.
    '''
    def parse_words(self, input_string, stem=True):
        word_pattern = re.compile(r'[0-9a-zA-Z]+')
        words = []
        tokens = re.findall(word_pattern, input_string)
        tokens = [t.lower() for t in tokens]
        stemmer = PorterStemmer()
        for token in tokens:
            if len(token) < self.min_length or token in self.stopwords or token.isdigit():
                continue
            word = stemmer.stem(token.lower()) if stem else token.lower()
            if self._is_valid(word):
                words.append(word)
        return words


    def _is_valid(self, word):
        #  Check whether the word is too short
        if(len(word) < self.min_length):
            return False
        #  Check whether the word is a stop word
        if(word in self.stopwords):
            return False
        return True


if __name__ == '__main__':
    s1 = '''
        Recovery excitement brings Mexican markets to life. Emerging evidence
        that Mexico's economy was back on the recovery track sent Mexican
        markets into a buzz of excitement Tuesday, with stocks closing at record
        highs and interest rates at 19-month lows."Mexico has been trying to
        stage a recovery since the beginning of this year and it's always been
        getting ahead of itself in terms of fundamentals," said Matthew Hickman
        of Lehman Brothers in New York."Now we're at the point where the
        fundamentals are with us. The history is now falling out of view."That
        history is one etched into the minds of all investors in Mexico: an
        economy in crisis since December 1994, a free-falling peso and
        stubbornly high interest rates.This week, however, second-quarter gross
        domestic product was reported up 7.2 percent, much stronger than most
        analysts had expected. Interest rates on governent Treasury bills, or
        Cetes, in the secondary market fell on Tuesday to 23.90 percent, their
        lowest level since Jan. 25, 1995.The stock market's main price index
        rallied 77.12 points, or 2.32 percent, to a record 3,401.79 points, with
        volume at a frenzied 159.89 million shares.Confounding all expectations
        has been the strength of the peso, which ended higher in its longer-term
        contracts on Tuesday despite the secondary Cetes drop and expectations
        of lower benchmark rates in Tuesday's weekly auction.With U.S. long-term
        interest rates expected to remain steady after the Federal Reserve
        refrained from raising short-term rates on Tuesday, the attraction of
        Mexico, analysts say, is that it offers robust returns for foreigners
        and growing confidence that they will not fall victim to a crumbling
        peso."The focus is back on Mexican fundamentals," said Lars Schonander,
        head of researcher at Santander in Mexico City. "You have a continuing
        decline in inflation, a stronger-than-expected GDP growth figure and the
        lack of any upward move in U.S. rates."Other factors were also at play,
        said Felix Boni, head of research at James Capel in Mexico City, such as
        positive technicals and economic uncertainty in Argentina, which has put
        it and neighbouring Brazil's markets at risk."There's a movement out of
        South American markets into Mexico," he said. But Boni was also wary of
        what he said could be "a lot of hype."The economic recovery was still
        export-led, and evidence was patchy that the domestic consumer was back
        with a vengeance. Also, corporate earnings need to grow str
        '''
    wp = TextParser(stopword_file = 'stopwords.txt')
    print wp.parse_words(s1)

