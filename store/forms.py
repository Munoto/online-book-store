from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book, Author, Genre


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
        fields = ['title', 'authors', 'genres', 'price', 'stock', 'description', 'cover_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'cover_image': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=True,
        label="Авторы",
        help_text="Выберите одного или нескольких авторов"
    )

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=True,
        label="Жанры",
        help_text="Выберите один или несколько жанров"
    )

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



class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {'name': 'Жанр'}



class ShippingForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        label='Адрес доставки',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш адрес'
        })
    )
    city = forms.CharField(
        max_length=100,
        label='Город',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш город'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        label='Почтовый индекс',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш почтовый индекс'
        })
    )