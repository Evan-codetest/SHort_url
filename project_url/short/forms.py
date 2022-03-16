from logging import PlaceHolder
from django import forms

class url_form(forms.Form):
    url_data = forms.URLField(label='URL',widget=forms.URLInput,empty_value=None,required=True)

class custom_form(forms.Form):
    url_data = forms.URLField(label='URL',widget=forms.URLInput,empty_value=None,required=True)
    word = forms.CharField(label='Custom words(< 10 letters)',widget=forms.TextInput, max_length=10, required=True)