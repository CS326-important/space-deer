from django.core.management.base import BaseCommand
from textifai.models import User, Text, Insight, Comment, GeneralInsight, GrammaticalInsight
import uuid
from datetime import datetime

class Command(BaseCommand):
    args = '<>'
    help = 'Run this script to populate database w/ sample users.'
    user1 = None
    user2 = None
    user3 = None
    text1 = None
    text2 = None
    text3 = None

    def create_users(self):
        self.user1 = User(username='tom', email='tomthebomb@hotmail.com')
        self.user1.save()
        self.user2 = User(username='michelle', email='shipluvr@aol.net')
        self.user2.save()
        self.user3 = User(username='William Shakespeare', email='billshakes@gmail.com')
        self.user3.save()
        self.user4 = User(username='Steve', email='coffee4steve@gmail.com')
        self.user4.save()

    def create_texts(self):
        self.text1 = Text(content='Wherefore art thou, Romeo?', user=self.user1, mature_content = False)
        self.text1.save()
        self.text2 = Text(title='Salty Sailor', content='I\'m going to attack you with a ship', user=self.user2, mature_content = True)
        self.text2.save()
        self.text3 = Text(content="""
            Ham. O, I die, Horatio; The potent poison quite oer-crows my spirit:
            I cannot live to hear the news from England; But I do prophesy the election
            lights On Fortinbras: he has my dying voice; So tell him, with the occurrents,
            more and less, Which have solicited. the rest is silence. [Dies.] Hor.
            Now cracks a noble heart. Good night, sweet prince, And flights of angels
            sing thee to thy rest! Why does the drum come hither? [March within.]"
            """
                          , user=self.user1
                          , mature_content = False
        )
        self.text3.save()
        self.text4 = Text(title="Espresso", content="""
        Extraction, iced siphon aroma to go, that filter percolator a beans. Steamed
        carajillo con panna est con panna arabica est filter extra. Grounds ristretto
        macchiato id sweet, spoon cinnamon black carajillo aromatic. Siphon caffeine,
        brewed blue mountain americano blue mountain extra blue mountain. In, percolator
        froth est ut pumpkin spice seasonal so redeye breve. Milk cappuccino cup, cinnamon
        wings cinnamon milk sweet. Brewed café au lait, java, caffeine, ristretto, siphon
        doppio body organic eu that. Et, barista whipped kopi-luwak percolator single origin
        skinny rich fair trade. Coffee galão sugar cappuccino sit carajillo cup milk kopi-luwak aroma.
        """, user = self.user4, mature_content = False)
        self.text4.save()

    def create_insights(self):
        insight1 = Insight(tone='Sad', probability=0.93, text=self.text1, user=self.user1)
        insight1.save()
        insight2 = Insight(tone='Violent', probability=0.83, text=self.text2, user=self.user2)
        insight2.save()
        insights = [('Negative', 0.69), ('Shakespeare', 0.92), ('Death', 0.99),
                    ('Politics', 0.84), ('Music', 0.51)]
        self.add_list_of_insights(insights, self.text3, self.user1)

    def add_list_of_insights(self, insights, text, user):
        """
        Helper method for adding a list of insights to an associated text and user.
        Takes a list of (tone, probability) tuples.
        """
        for t in insights:
            Insight(tone=t[0], probability=t[1], text=text, user=user).save()

    def create_comments(self):
        comment1 = Comment(content='I like this text.', text=self.text2, user=self.user1)
        comment1.save()
        comment2 = Comment(content='You can reduce the violence of this text by replacing "attack" with something more positive, like "bring you to Hawaii".', text=self.text1, user=self.user2)
        comment2.save()
        Comment(content="Cool! Did you write this? :^)", text=self.text3,
                user=self.user2).save()
        Comment(content="yeah. I should try to make it more positive though.",
                text=self.text3, user=self.user1).save()
        Comment(content="This is a pretty solid analysis.",
                text=self.text3, user=self.user3).save()

    def create_general_insights(self):
        gen_insight1 = GeneralInsight(name="Global Happiness",value="High")
        gen_insight1.save()
        gen_insight2 = GeneralInsight(name="Global Violence",value="Very High")
        gen_insight2.save()

    def create_grammaticalinsights(self):
        GrammaticalInsight(user=self.user1
                           , text=self.text3
                           , positivity='Low'
                           , most_common_pos=GrammaticalInsight.NOUN
                           , reading_level='9-10th Grade'
                           , reading_time='18 seconds'
                           , speaking_time='27 seconds'
                           , total_words=79
                           , total_chars=439
                           , most_common_word='the'
                           , average_word_length=4
                           ).save()

    def handle(self, *args, **options):
        self.create_users()
        self.create_texts()
        self.create_insights()
        self.create_comments()
        self.create_general_insights()
        self.create_grammaticalinsights()