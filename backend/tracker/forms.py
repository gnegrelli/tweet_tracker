from django.forms import CharField, ModelForm, Textarea

from .models import Tweet


class TweetForm(ModelForm):
    content = CharField(widget=Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = Tweet
        fields = '__all__'
