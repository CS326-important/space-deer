from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from .models import User, Text, Insight, Comment, GeneralInsight, \
    GrammaticalInsight
from .modules import gic, textanalyzer
from .forms import *
import random


# Create your views here.

def index(request):
    """
    View function for the homepage of the site
    """
    recent = Text.objects.all()[:4]
    return render(request, 'index.html', context={'recent': recent})


def _save_insights(insights, text, user):
    [Insight(tone=x[0], probability=x[1], text=text, user=user).save() for x in insights]

def _save_grammatical_insight(analysis, text, user):
    GrammaticalInsight(user=user
                       , text=text
                       , positivity=analysis.get_sentiment()
                       , most_common_pos=analysis.get_most_common_pos()
                       , reading_level=analysis.get_reading_level()
                       , reading_time=analysis.get_reading_time()
                       , speaking_time=analysis.get_speaking_time()
                       , total_words=analysis.get_total_words()
                       , total_chars=analysis.get_total_characters()
                       , most_common_word=analysis.get_most_common_word()
                       , average_word_length=analysis.get_average_word_length()
                       , total_sentences= analysis.get_num_sentences()
                      ).save()


def _save_text_analysis(user, analysis):
    text = Text(content=analysis.text, user=user, mature_content=False)
    text.save()

    _save_insights(analysis.get_insights(), text, user)
    _save_grammatical_insight(analysis, text, user)
    return text.m_id


def _edit_text_analysis(original_text, user, analysis):
    _delete_all_insights(original_text)

    original_text.content = analysis.text
    original_text.save()

    _save_insights(analysis.get_insights(), original_text, user)
    _save_grammatical_insight(analysis, original_text, user)


def _delete_all_insights(text):
    Insight.objects.filter(text=text).delete()
    GrammaticalInsight.objects.filter(text=text).delete()


@login_required
def textinput(request):
    """
    View function for the text input page of the site.
    """
    if request.method == 'POST':
        if len(request.FILES) != 0:
            form = FileUploadForm(request.POST)
            file = request.FILES['file']
            if form.is_valid():
                return _submit_text_file(form, file, request.user)
        else:
            form = TextAnalysisForm(request.POST)
            if form.is_valid():
                return _submit_text(form, request.user)

    return render(request, 'textinput.html', context={},)

    
def _submit_text(form, user):
    text = form.cleaned_data['text_analysis_input']
    text_analysis = textanalyzer.TextAnalyzer(text)
    m_id = _save_text_analysis(user, text_analysis)
    return HttpResponseRedirect(reverse('featureoutput', args=(m_id,)))


def _submit_comment(form, text, user):
    comment_text = form.cleaned_data['comment_input']
    Comment(content=comment_text, text=text, user=user).save()
    return HttpResponseRedirect(reverse('featureoutput', args=(text.m_id,)))


def _submit_edited_text(form, text, user):
    edited_text = form.cleaned_data['edited_text']
    text_analysis = textanalyzer.TextAnalyzer(edited_text)
    _edit_text_analysis(text, user, text_analysis)
    return HttpResponseRedirect(reverse('featureoutput', args=(text.m_id,)))

    
def _submit_text_file(form, file, user):
    file_text = form.cleaned_data['file_upload']
    text_analysis = textanalyzer.TextAnalyzer(file_text)
    m_id = _save_text_analysis(user, text_analysis)
    return HttpResponseRedirect(reverse('featureoutput', args=(m_id,)))

    
def _post_featureoutput(request, text): 
    if request.POST.get("new_submission_button"):
        return redirect('textinput')

    if request.POST.get("edit_submission_button"):
        form = EditedTextForm(request.POST)
        if form.is_valid():
            return _submit_edited_text(form, text, request.user)

    if request.POST.get("comment_input_button"):
        form = CommentInputForm(request.POST)
        if form.is_valid():
            return _submit_comment(form, text, request.user)

    return HttpResponseRedirect(reverse('featureoutput', args=(text.m_id,)))


def _render_featureoutput(request, text):
    context_dict = {
        'text': text,
        'author': text.user,
        'insights': Insight.objects.filter(text=text),
        'g_insights': GrammaticalInsight.objects.filter(text=text).first(),
        'comments': Comment.objects.filter(text=text),}
    return render(request, 'featureoutput.html', context=context_dict)


def featureoutput(request, pk):
    """
    View function for the feature output page of the site.
    """
    text = get_object_or_404(Text, pk=pk)
    return _post_featureoutput(request, text) if request.method == 'POST' else\
        _render_featureoutput(request, text)


@login_required
def account(request):
    """
    View function for user accounts.
    """
    if request.user.is_authenticated:
        texts = Text.objects.filter(user=request.user)[:3]
        comments = Comment.objects.filter(user=request.user)[:3]
        analytics = Insight.objects.filter(user=request.user).values('tone').annotate(Avg('probability')).order_by('-probability__avg')[:5]
    return render(
        request,
        "account.html",
        context={'user': request.user, 'texts': texts, 'comments': comments,
                 'analytics': analytics}
    )


def general_insights(request):
    """
    View function for the general insights page of the site.
    """
    gic.calc_and_save_general_insights()
    insights = GeneralInsight.objects.order_by('?')
    true_personal_insights = dict()

    if request.user.is_authenticated:
        personal_insights = Insight.objects.filter(user=request.user,
                    text__isnull=False)

        true_personal_insights = dict()

        for tone in set([ insight.tone for insight in personal_insights ]):
            try:
                true_personal_insights[tone] = sum([ insight.probability
                        for insight in personal_insights
                        if insight.tone == tone ]) / len([ insight
                        for insight in personal_insights
                        if insight.tone == tone ])

            except ZeroDivisionError:
                continue

            true_personal_insights[tone] = int(true_personal_insights[tone]
                    * 100)

        true_personal_insights = list(true_personal_insights.items())
        random.shuffle(true_personal_insights)
    else:
        true_personal_insights = []

    return render(
        request,
        'general-insights.html',
        context={
            'insights': insights,
            'personal_insights': true_personal_insights[:4]
        },
    )

