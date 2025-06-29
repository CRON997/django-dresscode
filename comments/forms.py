from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=400,
                           widget=forms.TextInput(
                               attrs={'rows': 4, 'id': 'comment-input', 'placeholder': 'Write your review...'}))

    class Meta:
        model = Comment
        fields = ('text',)
