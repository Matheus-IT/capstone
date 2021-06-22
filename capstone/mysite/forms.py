from django import forms
from .models import UserFeedback


class GiveFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ('title', 'content')
