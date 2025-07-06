from django import forms
from .models import User

class SigninForm(forms.Form):
    email = forms.EmailField(label="Your e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Your password")

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'date_of_birth']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Пароли не совпадают")

class EditProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'date_of_birth', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Пароли не совпадают")
