from django import forms

class TagForm(forms.Form):
    tag_key = forms.CharField(label='Tag Key', max_length=100)
    #tag_value = forms.CharField(label='Tag Value', max_length=100)
    