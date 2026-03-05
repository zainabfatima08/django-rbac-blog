from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic','article']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-400',
                'placeholder': 'Enter topic...'
            }),
            'article': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:border-blue-400',
                'placeholder': 'Write your article...',
                'rows': 6
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'class' : 'w-full border rounded p-2',
                'rows' : 3,
                'placeholder': 'Enter Your Comment Here!'

            })
            
        }
