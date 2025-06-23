from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=400,
                           widget=forms.TextInput(attrs={'class': 'comment-form', 'placeholder': 'Enter comment'}))

    class Meta:
        model = Comment
        fields = ('text',)
