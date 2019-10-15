from django import forms
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label="Username")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'hidden'}),required=False)
    class Meta:
        model = User
        fields = [ 'username','email']


class ProfileUpdateForm(ModelForm):
    # image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}), label="Image")
    work = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label="Carrier/Work")

    class Meta:
        model = Profile
        fields = [ 'image','work']

class passwordForm(PasswordChangeForm):
    old_password = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}), label="Old Password")
    new_password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}), label="NewPassword")
    new_password2 =forms.CharField(widget= forms.PasswordInput(attrs={'class':'form-control'}), label="Confirm Password")

    class Meta:
        modal = User
        fields = ['old_password','new_password1','new_password2']
    