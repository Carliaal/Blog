from django import forms

from .models import Comment


class AddCommmentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('alias', 'content')
