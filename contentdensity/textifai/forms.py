from django import forms


class TextAnalysisForm(forms.Form):
    text_analysis_input = forms.CharField()
