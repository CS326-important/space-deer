from django.shortcuts import render
from django.db.models import Q
from .models import User, Text, Insight, Comment, GeneralInsight, GrammaticalInsight
from .modules import gic

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
    mock_user = User.objects.all()[0]
    mock_text = Text.objects.filter(user=mock_user)[1]
    mock_insights = Insight.objects.filter(text=mock_text)
    g_insights = GrammaticalInsight.objects.filter(text=mock_text).first()
    comments = Comment.objects.filter(text=mock_text)
    return render(
        request,
        'featureoutput.html',
        context={'mock_text': mock_text.content
            , 'mock_insights': mock_insights
            , 'g_insights': g_insights
            , 'comments': comments},
    )

def account(request):
    """
    View function for user accounts.
    """
    mock_user = User.objects.first()
    texts = Text.objects.filter(user=mock_user)
    comments = Comment.objects.filter(user=mock_user)
    analytics = Insight.objects.filter(user=mock_user)
    return render(
        request,
        "account.html",
        context={'user':mock_user,'texts':texts,'comments':comments,'analytics':analytics}
    )

def general_insights(request):
    """
    View function for the general insights page of the site.
    """
    gic.calc_and_save_general_insights()
    insights = GeneralInsight.objects.order_by('?')
    # TODO: personal contributions to the general insights
    personal_insights = Insight.objects.filter(user=None, text__isnull=False)
    username=None
    return render(
        request,
        'general-insights.html',
        context={'insights':insights, 'personal_insights':personal_insights, 'username':username},
    )

