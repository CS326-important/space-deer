from django.shortcuts import render
from django.db.models import Q
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
    mock_text = Text.objects.first()
    mock_insights = Insight.objects.filter(user=mock_text.user)
    return render(
        request,
        'featureoutput.html',
        context={'mock_text': mock_text.content, 'mock_insights': mock_insights},
    )

def account(request):
    """
    View function for user accounts.
    """    
    texts = Text.objects.first()
    text_str = str(texts)
    max_length = 150
    if (len(text_str) > max_length):
        text_str = (text_str[:max_length] + "...")
        
    username = User.objects.first()
    comments = Comment.objects.first()
    analytics = Insight.objects.filter(user=User.objects.first())
    return render(
        request,
        "account.html",
        context={'username':username,'texts':text_str,'comments':comments,'analytics':analytics}
    )

def general_insights(request):
    """
    View function for the general insights page of the site.
    """
    insights = Insight.objects.filter(user__isnull=True, text__isnull=True)
    # TODO: personal contributions to the general insights
    personal_insights = Insight.objects.filter(user=None, text__isnull=False)
    username=None
    return render(
        request,
        'general-insights.html',
        context={'insights':insights, 'personal_insights':personal_insights, 'username':username},
    )

