from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class User(models.Model):
    """
    Model representing a user account.
    """
    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this user.")
    email = models.CharField(max_length=40)
    username = models.CharField(max_length=20)

    """
    User settings.
    """
    LIGHT = 'LI'
    DARK = 'DA'
    THEMES = (
        (LIGHT, 'Light'),
        (DARK, 'Dark'),
    )
    theme = models.CharField(max_length=2, choices=THEMES, default=LIGHT)

    def get_absolute_url(self):
        """
        Returns the url to access a particular User instance.
        """
        return reverse('user-detail', args=[str(self.m_id)])

    def __str__(self):
        """
        String for representing the User object.
        """
        return self.username


class Text(models.Model):
    """
    Model representing text from user input.
    """
    m_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular text.")
    content = models.TextField( help_text="Enter text here")
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    mature_content = models.BooleanField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular Text instance.
        """
        return reverse('text-detail', args=[str(self.m_id)])

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
    name = models.CharField(primary_key=True, max_length=24)
    value = models.CharField(max_length=24)

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

