import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from functools import reduce
import indicoio

indicoio.config.api_key = '662e01cb3f997caf914df39a89bf0075'


class TextAnalyzer:
    def __init__(self, text_input):
        self.text = text_input
        self.insights = self._get_insights()
        self.sentiment = self._get_sentiment()
        self.most_common_pos = self._get_most_common_pos()
        self.reading_level = self._get_reading_level()
        self.reading_time = self._get_reading_time()
        self.speaking_time = self._get_speaking_time()
        self.total_words = len(self.text.split())
        self.total_characters = len(self.text)
        self.most_common_word = self._get_most_common_word()
        self.average_word_length = self._get_average_word_length()

    def _get_insights(self):
        insights = []
        insights += self._get_text_tag()
        insights += self._get_emotions()
        insights += self._get_personality()
        return insights

    def _get_text_tag(self):
        tags = indicoio.text_tags(self.text)
        key = self._arg_max(tags)
        return [(key, tags[key])]

    def _get_sentiment(self):
        scores = SentimentIntensityAnalyzer().polarity_scores(self.text)
        return self._arg_max(scores)

    def _arg_max(self, d):
        return max(d.keys(), key=lambda k: d[k])

    def _get_emotions(self):
        return list(indicoio.emotion(self.text).items())

    def _get_personality(self):
        return list(indicoio.personality(self.text).items())

    def _get_most_common_pos(self):
        pos_list = [t[1] for t in nltk.pos_tag(nltk.word_tokenize(self.text))]
        return Counter(pos_list).most_common(1)[0][0]

    def _get_reading_level(self):
        # todo
        return None

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

    def _get_reading_time(self):
        """
        Based on an average reading speed of 200 wpm.
        """
        return self._format_time_string(self._convert_text_to_seconds(200))

    def _get_speaking_time(self):
        """
        Based on average speaking speed of 150 wpm.
        """
        return self._format_time_string(self._convert_text_to_seconds(150))

    def _get_most_common_word(self):
        return Counter(self.text.split()).most_common(1)[0][0]

    def _get_average_word_length(self):
        word_list = self.text.split()
        return reduce(lambda x, y: x + len(y), word_list, 0) / len(word_list)
