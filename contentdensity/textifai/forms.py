from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class TextAnalysisForm(forms.Form):
    text_analysis_input = forms.CharField()

    def clean_text_analysis_input(self):
        data = self.cleaned_data['text_analysis_input']
        if not data:
            raise ValidationError(
                _('Invalid text - tried to submit empty input'))
        return data


class CommentInputForm(forms.Form):
    comment_input = forms.CharField()

    def clean_comment_input(self):
        data = self.cleaned_data['comment_input']
        if not data:
            raise ValidationError(
                _('Invalid comment - tried to submit an empty comment'))
        return data
