from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import datetime

# Create your models here.

class Text(models.Model):
    """
    Model representing text from user input.
    """
    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular text.")
    title = models.CharField(max_length=40,  blank=True, help_text="Enter a title for your entry")
    content = models.TextField(help_text="Enter text here")
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    mature_content = models.BooleanField()

    class Meta:
        ordering = ["-time_created"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular Text instance.
        """
        return reverse('featureoutput', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the Text object.
        """
        return self.content


class Insight(models.Model):
    """
    Model representing an insight associated with text.
    """
    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular insight.")
    tone = models.CharField(max_length=100)
    probability = models.FloatField()
    text = models.ForeignKey(Text)
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        """
        Returns the url to access a particular Insight instance.
        """
        return reverse('insight-detail', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the Insight object.
        """
        return self.tone

class GrammaticalInsight(models.Model):
    """
    Model representing a grammatical insight associated with text.
    """
    ADJECTIVE = 'ADJ'
    ADPOSITION = 'ADP'
    ADVERB = 'ADV'
    CONJUNCTION = 'CONJ'
    DETERMINER = 'DET'
    NOUN = 'NOUN'
    NUMERICAL = 'NUM'
    PARTICLE = 'PRT'
    PRONOUN = 'PRO'
    VERB = 'VERB'
    PUNCTUATION = '.'
    OTHER = 'X'

    PARTS_OF_SPEECH = (
        (ADJECTIVE, 'Adjective'),
        (ADPOSITION, 'Adposition'),
        (ADVERB, 'Adverb'),
        (CONJUNCTION, 'Conjunection'),
        (DETERMINER, 'Determiner'),
        (NOUN, 'Noun'),
        (NUMERICAL, 'Numerical'),
        (PARTICLE, 'Particle'),
        (PRONOUN, 'Pronoun'),
        (VERB, 'Verb'),
        (PUNCTUATION, 'Punctuation'),
        (OTHER, 'Other'),
    )

    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4
                            , help_text="Unique ID for GrammaticalInsight.")
    user = models.ForeignKey(User)
    text = models.ForeignKey(Text)

    positivity = models.CharField(max_length=24)
    most_common_pos = models.CharField(max_length=4, choices=PARTS_OF_SPEECH)
    reading_level = models.CharField(max_length=100)
    reading_time = models.CharField(max_length=100)
    speaking_time = models.CharField(max_length=100)
    total_words = models.IntegerField()
    total_chars = models.IntegerField()
    total_sentences = models.IntegerField()
    most_common_word = models.CharField(max_length=100)
    average_word_length = models.IntegerField()


    def get_absolute_url(self):
        """
        Returns the url to access a particular GrammaticalInsight instance.
        """
        return reverse('grammaticalinsight-detail', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the GrammaticalInsight object.
        """
        return "positivity: {}, most_common_pos: {}, reading_level: {}, " \
               "reading_time: {}, speaking_time: {}, total_words: {}, " \
               "total_chars: {}, most_common_word: {}, average_word_length: {}" \
               "".format(self.positivity
                         , self.most_common_pos
                         , self.reading_level
                         , self.reading_time
                         , self.speaking_time
                         , self.total_words
                         , self.total_chars
                         , self.most_common_word
                         , self.average_word_length)

class Comment(models.Model):
    """
    Model representing a comment associated with text and a user.
    """
    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular comment.")
    content = models.TextField(max_length=500)
    text = models.ForeignKey(Text)
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def get_absolute_url(self):
        """
        Returns the url to access a particular Comment instance.
        """
        return reverse('comment-detail', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the Comment object.
        """
        return self.content

class GeneralInsight(models.Model):
    """
    Model representing a general insight
    """
    name = models.CharField(primary_key=True, max_length=127)
    value = models.CharField(max_length=127, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular GeneralInsight instance.
        """
        return reverse('gen-insight-detail', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the GeneralInsight object.
        """
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        super(type(self), self).save(*args, **kwargs)

    def clean(self):
        self.name = self.name.strip()
        self.value = self.value.strip()

