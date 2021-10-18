from django import forms
from .models import UserFeedback


class GiveFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'id': 'feedback-content',
                    'class': 'feedback-submit-content',
                    'placeholder': 'Give feedback...',
                    'cols': 10,
                    'rows': 6,
                    'required': True,
                }
            )
        }
