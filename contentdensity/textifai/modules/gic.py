
from functools import reduce
from ..models import User, Text, Insight, Comment, GeneralInsight

class general_insight_calculator:
    name = None
    calc = lambda *_: None

    def __init__(self, name, calc):
        self.name = name
        self.calc = calc

    def do_calc(self):
        return self.calc()

    def calc_and_save(self):
        entry, created = GeneralInsight.objects.get_or_create(pk=self.name, defaults={'value':''})
        entry.value = self.do_calc()
        entry.save()

# Dictionary of general insight name to general insight calculator
general_insights = { }

def add_general_insight(name, func):
    global general_insights
    general_insights[name] = general_insight_calculator(name, func)

def calc_and_save_general_insights():
    for insight in general_insights.values():
        insight.calc_and_save()

########################################################################
# Insight calculation implementations
########################################################################

def _calc_total_words():
    ret = 0

    for text in Text.objects.all():
        ret += len(text.content.split())

    return ret

add_general_insight('Total Words', _calc_total_words)

