from django import forms
from django.forms import formset_factory
from django_summernote.widgets import SummernoteWidget
from django_summernote import fields as summer_fields
from .models import Convergence_Board, Convergence_Comment

class PostForm(forms.ModelForm):
    class Meta:
           model = Convergence_Board
           fields = ('Board_Files',)
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['Board_Files'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Convergence_Comment
        fields = ['comment']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = "댓글"