from django import forms


class TextAnalysisForm(forms.Form):
    text_analysis_input = forms.CharField()


class CommentInputForm(forms.Form):
    comment_input = forms.CharField()
