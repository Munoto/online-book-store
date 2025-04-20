from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from store.forms import CustomUserCreationForm, CustomLoginForm, BookForm, AuthorForm
from store.models import Book


# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    books = Book.objects.all()  # Получаем все книги
    return render(request, 'home.html', {'books': books})

@login_required
def create_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа к этой странице.")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BookForm()
    return render(request, 'create_book.html', {'form': form})


@login_required
def create_author(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа к этой странице.")

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('create_book.html')
    else:
        form = AuthorForm()
    return render(request, 'create_author.html', {'form': form})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})