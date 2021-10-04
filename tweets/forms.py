from django.conf import settings

from .models import Tweet
from django import forms

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ("content",)

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("Tweet too long")
        return content