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


class EditedTextForm(forms.Form):
    edited_text = forms.CharField()

    def clean_edited_text(self):
        data = self.cleaned_data['edited_text']
        return data


class FileUploadForm(forms.Form):
    file = forms.FileField()
    
    def clean_text_analysis_input(self):
        self.file.open(mode='rb') 
        data = self.file.readlines()
        self.file.close()
        if not data:
            raise ValidationError(
                _('Invalid text - tried to upload empty file'))
        return data