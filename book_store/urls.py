from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from book_store import settings
from store.views import logout_view, home_view, register_view, login_view, create_author, create_book, book_detail, \
    edit_book, delete_book, add_to_cart, cart_view, clear_cart, remove_from_cart, create_genre, update_quantity, \
    genre_books, author_detail, shipping_view, order_success_view, profile_view, order_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_book/', create_book, name='create_book'),
    path('books/<int:pk>/edit/', edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', delete_book, name='delete_book'),
    path('create_author/', create_author, name='create_author'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('create_genre/', create_genre, name='create_genre'),
    path('cart/update_quantity/<int:cart_item_id>/', update_quantity, name='update_quantity'),
    path('genre/<int:genre_id>/', genre_books, name='genre_books'),
    path('author/<int:author_id>/', author_detail, name='author_detail'),
    path('shipping/', shipping_view, name='shipping'),
    path('order-success/', order_success_view, name='order_success'),
    path('profile/', profile_view, name='profile'),
    path('order/<int:order_id>/', order_detail_view, name='order_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
