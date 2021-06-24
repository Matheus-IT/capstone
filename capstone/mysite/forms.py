from django import forms
from .models import UserFeedback


class GiveFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'class': 'feedback-submit-content',
                                             'placeholder': 'Give feedback...',
                                             'cols': 30, 
                                             'rows': 6})
        }
