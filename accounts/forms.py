# accounts/forms.py
from django import forms

class ClaimsForm(forms.Form):
    claim_type = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    document = forms.FileField(required=False)