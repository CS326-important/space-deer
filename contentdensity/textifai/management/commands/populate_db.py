from django.core.management.base import BaseCommand
from textifai.models import User, Text, Insight, Comment, GeneralInsight
import uuid
from datetime import datetime

class Command(BaseCommand):
    args = '<>'
    help = 'Run this script to populate database w/ sample users.'
    user1 = None
    user2 = None
    text1 = None
    text2 = None
    text3 = None

    def create_users(self):
        self.user1 = User(m_id=uuid.uuid4(), username='tom', email='tomthebomb@hotmail.com')
        self.user1.save()
        self.user2 = User(m_id=uuid.uuid4(), username='michelle', email='shipluvr@aol.net')
        self.user2.save()

    def create_texts(self):
        self.text1 = Text(m_id=uuid.uuid4(), content='Wherefore art thou, Romeo?', time_created=datetime.now(), user=self.user1, mature_content = False)
        self.text1.save()
        self.text2 = Text(m_id=uuid.uuid4(), content='I\'m going to attack you with a ship', time_created=datetime.now(), user=self.user2, mature_content = True)
        self.text2.save()
        self.text3 = Text(m_id=uuid.uuid4()
                          , content="""
            Ham. O, I die, Horatio; The potent poison quite oer-crows my spirit:
            I cannot live to hear the news from England; But I do prophesy the election
            lights On Fortinbras: he has my dying voice; So tell him, with the occurrents,
            more and less, Which have solicited. the rest is silence. [Dies.] Hor.
            Now cracks a noble heart. Good night, sweet prince, And flights of angels
            sing thee to thy rest! Why does the drum come hither? [March within.]"
            """
                          , time_created=datetime.now()
                          , user=self.user1
                          , mature_content = False
        )
        self.text3.save()

    def create_insights(self):
        insight1 = Insight(m_id=uuid.uuid4(), tone='Sad', probability=0.93, text=self.text1, user=self.user1)
        insight1.save()
        insight2 = Insight(m_id=uuid.uuid4(), tone='Violent', probability=0.83, text=self.text2, user=self.user2)
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
            Insight(m_id=uuid.uuid4(), tone=t[0], probability=t[1], text=text, user=user).save()

    def create_comments(self):
        comment1 = Comment(m_id=uuid.uuid4(), content='I like this text.', text=self.text2, time_created=datetime.now(), user=self.user1)
        comment1.save()
        comment2 = Comment(m_id=uuid.uuid4(), content='You can reduce the violence of this text by replacing "attack" with something more positive, like "bring you to Hawaii".', text=self.text1, time_created=datetime.now(), user=self.user2)
        comment2.save()

    def create_general_insights(self):
        gen_insight1 = GeneralInsight(name="Global Happiness",value="High")
        gen_insight1.save()
        gen_insight2 = GeneralInsight(name="Global Violence",value="Very High")
        gen_insight2.save()

    def handle(self, *args, **options):
        self.create_users()
        self.create_texts()
        self.create_insights()
        self.create_comments()
        self.create_general_insights()