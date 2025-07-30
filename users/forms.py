from django import forms
from .models import User

class SigninForm(forms.Form):
    email = forms.EmailField(
        label="Ваш e-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@example.com'
        })
    )
    password = forms.CharField(
        label="Ваш пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'date_of_birth']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия', 
            'email': 'Email',
            'password': 'Пароль',
            'date_of_birth': 'Дата рождения'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@example.com'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Минимум 8 символов'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Пароли не совпадают")
        
        return cleaned_data
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

class EditProfileForm(forms.ModelForm):
    password = forms.CharField(
        label="Новый пароль",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте пустым, если не хотите менять'
        }),
        help_text="Оставьте поле пустым, если не хотите менять пароль"
    )
    confirm_password = forms.CharField(
        label="Подтвердите новый пароль", 
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_of_birth']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email', 
            'date_of_birth': 'Дата рождения'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@example.com'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Проверяем пароли только если они заполнены
        if password or confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Пароли не совпадают")
        
        return cleaned_data
    
    def clean_email(self):
        """Проверка уникальности email (исключая текущего пользователя)"""
        email = self.cleaned_data.get('email')
        if email:
            # Проверяем, что email не занят другим пользователем
            existing_user = User.objects.filter(email=email).exclude(id=self.instance.id).first()
            if existing_user:
                raise forms.ValidationError("Пользователь с таким email уже существует")
        return email