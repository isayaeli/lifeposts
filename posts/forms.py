from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from posts.models import Post, Comment
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label="UserName")
    password = forms.CharField(widget=forms.PasswordInput(attrs= {'class':'form-control'}),label="PassWord")

class registerForm(UserCreationForm):
	username = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget= forms.EmailInput(attrs={'class':'form-control'}),label= "Email")
	password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}),label="Password")
	password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control','width':'30px'}),label="Confirm Password")
	
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

		def save(self, commit=True):
			user = super(registerForm, self).save(commit=False)
			user = self.cleaned_data['email']
			if commit:
				user.save()
			return user

class VideoForm(forms.Form):
	post_description = forms.CharField(widget=forms.TextInput(attrs={'class':'from-control'}), label="Caption")
	post_video = forms.FileField(widget=forms.FileInput(attrs={'class':'from-control','type':'file'}), label="Video")

	class Meta:
		model = Post
		fields = ['post_description', 'post_video']

class commentForm(forms.Form):
	contents = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label="Comment")

	class Meta:
		modal = Comment
		fields = ['contents']

