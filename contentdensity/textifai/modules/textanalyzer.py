import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from functools import reduce
import indicoio

indicoio.config.api_key = '662e01cb3f997caf914df39a89bf0075'


class TextAnalyzer(object):
    def __init__(self, text_input):
        self.text = text_input
        self.readable_sentiment = {
            'neu': 'neutral', 'pos': 'high', 'neg': 'low'}
        self.readable_pos = {
            '$': 'dollar',
            '\'\'': 'closing quotation mark',
            '(': 'opening parenthesis',
            ')': 'closing parenthesis',
            ',': 'comma',
            '--': 'dash',
            '.': 'sentence terminator',
            ':': 'colon or ellipsis',
            'CC': 'conjunction',
            'CD': 'numeral',
            'DT': 'determiner',
            'EX': 'existential there',
            'FW': 'foreign word',
            'IN': 'preposition',
            'JJ': 'adjective',
            'JJR': 'adjective',
            'JJS': 'adjective',
            'LS': 'list item marker',
            'MD': 'modal auxiliary',
            'NN': 'noun',
            'NNP': 'noun',
            'NNPS': 'noun',
            'NNS': 'noun',
            'PDT': 'pre-determiner',
            'POS': 'genitive marker',
            'PRP': 'pronoun',
            'PRP$': 'pronoun',
            'RB': 'adverb',
            'RBR': 'adverb',
            'RBS': 'adverb',
            'RP': 'particle',
            'SYM': 'symbol',
            'TO': 'to',
            'UH': 'interjection',
            'VB': 'verb',
            'VBD': 'verb',
            'VBG': 'verb',
            'VBN': 'verb',
            'VBP': 'verb',
            'VBZ': 'verb',
            'WDT': 'determiner',
            'WP': 'pronoun',
            'WP$': 'pronoun',
            'WRB': 'adverb',
            '``': 'opening quotation mark',
        }

    def get_insights(self):
        return (
            self._get_emotion(),
            self._get_personality(),
            self._get_political(),
        )  + self._get_text_tags(5)

    def _get_text_tags(self, n):
        return tuple(_get_max_n_tags(indicoio.text_tags(self.text), n))

    def _get_emotion(self):
        return _get_max_tag(indicoio.emotion(self.text))

    def _get_personality(self):
        return _get_max_tag(indicoio.personality(self.text))

    def _get_political(self):
        return _get_max_tag(indicoio.political(self.text))

    def get_sentiment(self):
        scores = SentimentIntensityAnalyzer().polarity_scores(self.text)
        scores.pop('compound')
        return self.readable_sentiment[_arg_max(scores)]

    def get_most_common_pos(self):
        pos_list = [t[1] for t in nltk.pos_tag(nltk.word_tokenize(self.text))]
        mc_pos = Counter(pos_list).most_common(1)[0][0]
        return self.readable_pos[mc_pos] if mc_pos in self.readable_pos else 'other'

    def get_reading_level(self):
        """
        https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula
        """

        readability_score = self._get_dale_chall_readability_score()

        if readability_score <= 4.9:
            return "4th grade"
        elif readability_score <= 5.9:
            return "5-6th grade"
        elif readability_score <= 6.9:
            return "7-8th grade"
        elif readability_score <= 7.9:
            return "9-10th grade"
        elif readability_score <= 8.9:
            return "11-12th grade"
        else:
            return "college"

    def _get_dale_chall_readability_score(self):
        word_list = self.text.split()
        return self._dale_chall_formula(
            self._get_num_difficult_words(word_list),
            self._get_num_sentences(),
            len(word_list))

    def _get_num_difficult_words(self, word_list):
        dale_chall_list = self._get_dale_chall_list()
        easy_words = set(reduce(lambda x, y: x + y, dale_chall_list).split())
        return reduce(
            lambda x, y: x + 1 if y not in easy_words else x, word_list, 0)

    def _get_dale_chall_list(self):
        with open('./textifai/modules/dale-chall-words.txt') as f:
            return f.readlines()

    def _get_num_sentences(self):
        return len(nltk.sent_tokenize(self.text))

    def _dale_chall_formula(self, difficult_words, sentences, words):
        adjusted = 3.6365 if difficult_words / words > 0.05 else 0
        return 0.1579 * ((difficult_words / words) * 100) \
            + 0.0496 * (words / sentences) + adjusted

    def _format_time_string(self, seconds):
        if seconds < 60:
            return str(round(seconds, 1)) + " seconds"
        elif seconds < 3600:
            return str(round(seconds / 60, 1)) + " minutes"
        elif seconds < 21600:
            return str(round(seconds / 3600, 1)) + " hours"
        else:
            return str(round(seconds / 86400, 1)) + " days"

    def _convert_text_to_seconds(self, wpm):
        return (len(self.text.split()) / wpm) * 60

    def get_reading_time(self):
        """
        Based on an average reading speed of 200 wpm.
        """
        return self._format_time_string(self._convert_text_to_seconds(200))

    def get_speaking_time(self):
        """
        Based on average speaking speed of 150 wpm.
        """
        return self._format_time_string(self._convert_text_to_seconds(150))

    def get_most_common_word(self):
        return Counter(self.text.split()).most_common(1)[0][0]

    def get_average_word_length(self):
        word_list = self.text.split()
        return reduce(lambda x, y: x + len(y), word_list, 0) / len(word_list)

    def get_total_characters(self):
        return len(self.text)

    def get_total_words(self):
        return len(self.text.split())


def _get_max_tag(tags):
    key = _arg_max(tags)
    return (key, tags[key])

def _get_max_n_tags(tags, n): 
    for x in range(n):
        key = _arg_max(tags)
        yield (key, tags[key])
        tags.pop(key)


def _arg_max(dictionary):
    return max(dictionary.keys(), key=lambda k: dictionary[k])
