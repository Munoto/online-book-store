from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from store.forms import CustomUserCreationForm, CustomLoginForm, BookForm, AuthorForm, GenreForm, ShippingForm
from store.models import Book, Author, Genre, Cart, CartItem, OrderItem, Order


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
    genres = Genre.objects.all()

    authors = Author.objects.all()

    genre_id = request.GET.get('genre_id')
    books = Book.objects.all()

    if genre_id:
        genre = Genre.objects.get(id=genre_id)
        books = books.filter(genre=genre)

    return render(request, 'home.html', {'genres': genres, 'books': books, 'authors': authors})


def create_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа к этой странице.")

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()

            book.author.set(form.cleaned_data['authors'])
            book.genre.set(form.cleaned_data['genres'])
            book.save()

            return redirect('home')
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
            return redirect('create_book')
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


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    books = cart.items.all()
    total_price = cart.total_price()

    context = {
        'books': books,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_view')


def create_genre(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа к этой странице.")

    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_book')
    else:
        form = GenreForm()

    return render(request, 'create_genre.html', {'form': form})


@login_required
def update_quantity(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id)

    if 'action' in request.POST:
        if request.POST['action'] == 'increase':
            item.quantity += 1
        elif request.POST['action'] == 'decrease' and item.quantity > 1:
            item.quantity -= 1


        item.save()

    return redirect('cart_view')


def genre_books(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    books = Book.objects.filter(genre=genre)
    return render(request, 'genre_books.html', {'genre': genre, 'books': books})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    books = author.book_set.all()

    return render(request, 'author_detail.html', {
        'author': author,
        'books': books,
    })


def shipping_view(request):
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']

            order = Order.objects.create(
                user=request.user,
                address=address,
                city=city,
                postal_code=postal_code,
            )

            cart_items = CartItem.objects.filter(cart__user=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price
                )
            cart_items.delete()

            return redirect('order_success')
    else:
        form = ShippingForm()

    return render(request, 'shipping.html', {'form': form})


def order_success_view(request):
    return render(request, 'order_success.html')


def profile_view(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'profile.html', {'orders': orders})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Получаем все элементы в заказе
    order_items = order.items.all()

    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})