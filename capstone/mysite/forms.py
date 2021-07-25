from django import forms
from .models import UserFeedback


class GiveFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'id': 'feedback-submit-content',
                                             'class': 'feedback-submit__content',
                                             'placeholder': 'Give feedback...',
                                             'cols': 30, 
                                             'rows': 6})
        }
