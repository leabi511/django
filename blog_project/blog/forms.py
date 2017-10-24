from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "text")
        widgets = {
            "title": forms.TextInput(),
            "text": forms.Textarea()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "editable medium-editor-textarea"})
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirmed_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        username = self.cleaned_data['username']
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Username %s is already in use.' % username)

        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address already exists.')

        password = self.cleaned_data.get('password')
        confirmed_password = self.cleaned_data.get('confirmed_password')
        if password and password != confirmed_password:
            raise forms.ValidationError("Passwords don't match.")
        return self.cleaned_data
