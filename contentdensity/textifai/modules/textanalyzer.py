import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from functools import reduce
import indicoio

indicoio.config.api_key = '662e01cb3f997caf914df39a89bf0075'


class TextAnalyzer(object):
    def __init__(self, text_input):
        self.text = text_input

    def get_insights(self):
        return self._get_text_tag() + \
            self._get_emotions() + \
            self._get_personality()

    def _get_text_tag(self):
        tags = indicoio.text_tags(self.text)
        key = _arg_max(tags)
        return ((key, tags[key]),)

    def _get_emotions(self):
        return tuple(indicoio.emotion(self.text).items())

    def _get_personality(self):
        return tuple(indicoio.personality(self.text).items())

    def get_sentiment(self):
        scores = SentimentIntensityAnalyzer().polarity_scores(self.text)
        return _arg_max(scores)

    def get_most_common_pos(self):
        pos_list = [t[1] for t in nltk.pos_tag(nltk.word_tokenize(self.text))]
        return Counter(pos_list).most_common(1)[0][0]

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


def _arg_max(dictionary):
    return max(dictionary.keys(), key=lambda k: dictionary[k])
