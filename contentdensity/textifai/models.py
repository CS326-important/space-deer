from django.db import models
from django.urls import reverse
import uuid

# Create your models here.


class Text(models.Model):
    """
    Model representing text from user input.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular text.")
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    #todo: userid, not required yet.

    def get_absolute_url(self):
        """
        Returns the url to access a particular Text instance.
        """
        return reverse('text-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Text object.
        """
        return self.content


class Insight(models.Model):
    """
    Model representing an insight associated with text.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular insight.")
    tone = models.CharField(max_length=100)
    probability = models.FloatField()
    text = models.ForeignKey(Text)

    def get_absolute_url(self):
        """
        Returns the url to access a particular Insight instance.
        """
        return reverse('insight-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Insight object.
        """
        return self.tone


class Comment(models.Model):
    """
    Model representing a model associated with text and a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular comment.")
    content = models.CharField(max_length=500)
    text = models.ForeignKey(Text)
    time = models.DateTimeField(auto_now_add=True)
    #todo: userid, not required yet.

    def get_absolute_url(self):
        """
        Returns the url to access a particular Comment instance.
        """
        return reverse('comment-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Comment object.
        """
        return self.content

