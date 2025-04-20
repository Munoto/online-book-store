from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book, Author


# Форма для регистрации:
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(username=email, password=password)
        if user is None:
            raise forms.ValidationError("Неверный email или пароль")
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'stock', 'description', 'cover_image']  # Указываем все нужные поля

        widgets = {
            'Название': forms.TextInput(attrs={'class': 'form-control'}),
            'Автор': forms.Select(attrs={'class': 'form-control'}),
            'Цена': forms.NumberInput(attrs={'class': 'form-control'}),
            'В наличии': forms.NumberInput(attrs={'class': 'form-control'}),
            'Описание': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'Обложка': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_date', 'biography', 'photo']
        widgets = {
            'ФИО': forms.TextInput(attrs={'class': 'form-control'}),
            'Дата рождения': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Биография': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'Фото автора': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }