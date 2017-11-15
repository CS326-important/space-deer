from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from .models import User, Text, Insight, Comment, GeneralInsight, \
    GrammaticalInsight
from .modules import gic, textanalyzer
from .forms import TextAnalysisForm


# Create your views here.

def index(request):
    """
    View function for the homepage of the site
    """
    recent = Text.objects.all()[:4]
    return render(request, 'index.html', context={'recent': recent})


def _save_analyzed_text(user, analysis):
    text = Text(content=analysis.text, user=user, mature_content=False)
    text.save()
    for t in analysis.insights:
        Insight(tone=t[0], probability=t[1], text=text, user=user).save()
    GrammaticalInsight(user=user
                       , text=text
                       , positivity=analysis.sentiment
                       , most_common_pos=analysis.most_common_pos
                       , reading_level="WIP"
                       , reading_time=analysis.reading_time
                       , speaking_time=analysis.speaking_time
                       , total_words=analysis.total_words
                       , total_chars=analysis.total_characters
                       , most_common_word=analysis.most_common_word
                       , average_word_length=analysis.average_word_length
                       ).save()
    return text.m_id


def textinput(request):
    """
    View function for the text input page of the site.
    """
    if request.method == 'POST':
        form = TextAnalysisForm(request.POST)

        if form.is_valid():
            text = form.data['text_analysis_input']
            text_analysis = textanalyzer.TextAnalyzer(text)
            user = User.objects.first()
            m_id = _save_analyzed_text(user, text_analysis)
            return HttpResponseRedirect(reverse('featureoutput', args=(m_id,)))

    return render(
        request,
        'textinput.html',
        context={},
    )


def featureoutput(request, pk):
    """
    View function for the feature output page of the site.
    """
    text = get_object_or_404(Text, pk=pk)
    insights = Insight.objects.filter(text=text)
    g_insights = GrammaticalInsight.objects.filter(text=text).first()
    comments = Comment.objects.filter(text=text)
    return render(
        request,
        'featureoutput.html',
        context={'text': text
            , 'insights': insights
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
        context={'user': mock_user, 'texts': texts, 'comments': comments,
                 'analytics': analytics}
    )


def general_insights(request):
    """
    View function for the general insights page of the site.
    """
    gic.calc_and_save_general_insights()
    insights = GeneralInsight.objects.order_by('?')
    # TODO: personal contributions to the general insights
    personal_insights = Insight.objects.filter(user=None, text__isnull=False)
    username = None
    return render(
        request,
        'general-insights.html',
        context={'insights': insights, 'personal_insights': personal_insights,
                 'username': username},
    )
