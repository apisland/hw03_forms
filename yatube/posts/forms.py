from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        text = forms.fields.CharField(widget=forms.Textarea)
        group = forms.ModelChoiceField(Post.objects.all(),
                                       required=False)


def clean_text(self):
    msg = self.cleaned_data['text']
    if 'text' not in msg:
        raise forms.ValidationError('Сообщение не может быть пустым!')
    return msg
