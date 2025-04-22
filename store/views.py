from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

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


@staff_member_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@staff_member_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'book': book})


@login_required(login_url='login')
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart = request.session.get('cart', {})

    if str(book_id) in cart:
        cart[str(book_id)] += 1
    else:
        cart[str(book_id)] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    books = []
    total_price = 0

    for book_id, quantity in cart.items():
        book = Book.objects.get(id=book_id)
        book.quantity = quantity
        book.total = book.price * quantity
        books.append(book)
        total_price += book.total

    context = {
        'books': books,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)


@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')


def remove_from_cart(request, book_id):
    cart = request.session.get('cart', {})
    if book_id in cart:
        del cart[book_id]
        request.session['cart'] = cart
    return redirect('cart')