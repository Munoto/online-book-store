from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from book_store import settings
from store.views import logout_view, home_view, register_view, login_view, create_author, create_book, book_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_book/', create_book, name='create_book'),
    path('create_author/', create_author, name='create_author'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
