from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms
from .models import User


class UserCreateForm(UserCreationForm):

    username = forms.CharField(max_length=50, required=True, help_text='Required.')
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        fields = ('email', 'username', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['username'].label = 'Username'
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class SetPassword(SetPasswordForm):

    class Meta:
        fields = ('new_password1', 'new_password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None