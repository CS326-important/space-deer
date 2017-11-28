
import string
from collections import Counter
from functools import partial
from ..models import User, Text, Insight, Comment, GeneralInsight

class general_insight_calculator:
    name = None
    calc = lambda *_: None

    def __init__(self, name, calc, *args):
        self.name = name
        self.calc = partial(calc, *args)

    def do_calc(self):
        return self.calc()

    def calc_and_save(self):
        entry, created = GeneralInsight.objects.get_or_create(pk=self.name,
                defaults={'value':''})
        entry.value = self.do_calc()
        entry.save()

# Dictionary of general insight name to general insight calculator
general_insights = { }

def add_general_insight(name, func, *args):
    global general_insights
    general_insights[name] = general_insight_calculator(name, func, *args)

def calc_and_save_general_insights():
    for insight in general_insights.values():
        insight.calc_and_save()

########################################################################
# Insight calculation implementations
########################################################################

def _calc_total_words():
    count = Counter()

    for text in Text.objects.all():
        count.update(list(filter(None, text.content.split())))

    return sum(count.values())

add_general_insight('Total Words', _calc_total_words)

def _calc_average_word_length():
    trans = str.maketrans('', '', string.punctuation)
    count = Counter()

    for text in Text.objects.all():
        count.update(list(filter(None,
                [ w.translate(trans) for w in text.content.split() ])))

    try:
        return str(sum(map(len, count.keys()))
                // len(count.keys())) + " letters"
    except ZeroDivisionError:
        return 'N/a'

add_general_insight('Average Word Length', _calc_average_word_length)

def _calc_average_entry_length():
    count = Counter()

    for text in Text.objects.all():
        count.update(list(filter(None, text.content.split())))

    try:
        return str(sum(count.values()) // len(Text.objects.all())) + " words"
    except ZeroDivisionError:
        return 'N/a'

add_general_insight('Average Entry Length', _calc_average_entry_length)

def _calc_total_entries():
    return len(Text.objects.all())

add_general_insight('Total Submitted Entries', _calc_total_entries)

def _calc_most_common_word():
    trans = str.maketrans('', '', string.punctuation)
    count = Counter()

    for text in Text.objects.all():
        count.update(list(filter(None,
                [ w.translate(trans) for w in text.content.split() ])))

    try:
        return count.most_common(1)[0][0]
    except IndexError:
        return 'N/a'

add_general_insight('Most Common Word', _calc_most_common_word)

def _calc_most_long_winded_user():
    trans = str.maketrans('', '', string.punctuation)
    count = Counter()

    for user in User.objects.all():
        count[user] = sum([sum(len(w.translate(trans))
                for w in text.content.split())
                for text in Text.objects.filter(user=user)])

        try:
            count[user] /= len(Text.objects.filter(user=user))
        except ZeroDivisionError:
            count[user] = 0

    try:
        return count.most_common(1)[0][0].username
    except IndexError:
        return 'N/a'

add_general_insight('Most Long-winded User', _calc_most_long_winded_user)

def _calc_most_published_user():
    count = Counter()

    for user in User.objects.all():
        count[user] = len(Text.objects.filter(user=user))

    try:
        return count.most_common(1)[0][0].username
    except IndexError:
        return 'N/a'

add_general_insight('Most Published User', _calc_most_published_user)

