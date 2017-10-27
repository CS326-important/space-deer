from django.shortcuts import render
from .models import User, Text, Insight, Comment

# Create your views here.

def index(request):
    """
    View function for the homepage of the site
    """
    return render(request, 'index.html', context={})

def textinput(request):
    """
    View function for the text input page of the site.
    """
    return render(
        request,
        'textinput.html',
        context={},
    )

def featureoutput(request):
    """
    View function for the feature output page of the site.
    """
    mock_text = Text.objects.all().first().content
    mock_insights = Insight.objects.all()
    print(mock_text)
    return render(
        request,
        'featureoutput.html',
        context={'mock_text': mock_text, 'mock_insights': mock_insights},
    )

from .models import User

def account(request):
    """
    View function for user accounts.
    """
    username = User._meta.get_field('username')
    return render(
        request,
        "account.html",
        context={'username':username}
    )