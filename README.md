# 📚 Online Bookstore (Django)

An online bookstore web application built with Django, allowing users to register, browse books, view details, and add them to a shopping cart. Admin users can manage books and authors through a user-friendly interface.

## 🔧 Features

- User registration & login
- Book listing & detail pages
- Shopping cart with quantity controls
- Admin panel to create, edit, and delete books and authors
- Conditional buttons and routes for admin users

## 🚀 Installation & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Munoto/online-book-store/
cd book_store
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

6. Run the Server
```bash
python manage.py runserver
```
Go to http://127.0.0.1:8000/ in your browser.

## 🧪 Modules
Module 1: User Registration
What it does: Registers a user and stores credentials.
How to use: Go to http://127.0.0.1:8000/register and register.

Module 2: User Login
What it does: Authenticates a user.
How to use: Go to http://127.0.0.1:8000/login/ and log in.

Module 3: Book Creation (Admin Only)
What it does: Allows admin to create a book.
How to use: After logging in as admin, click “Add Book” in the navbar.

Module 4: Author Creation (Admin Only)
What it does: Allows admin to create a new author.
How to use: While adding a book, click "Add Author" and fill out the form.

Module 5: Book Detail View
What it does: Shows full details of a book.
How to use: Click on any book card.

Module 6: Add to Cart
What it does: Adds book to user’s cart (requires login).
How to use: Click on the 🛒 icon. If not logged in, redirects to login page.

Module 7: View Cart
What it does: Displays books in the cart and allows editing quantity/removal.
How to use: Navigate to /cart/.


## 📦 Tech Stack
- Python 3
- Django 4
- SQLite (default database)
- Bootstrap 5
- HTML / CSS (via templates)


