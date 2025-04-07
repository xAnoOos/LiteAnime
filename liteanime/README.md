# 🌌 LiteAnime Platform

A modern community platform built with Django for anime, manga, and novel lovers.  
Users can register, log in, create threads, interact through comments, and manage their profiles.

---

## 🚀 Live Website

🌐 [liteanime.com](http://www.liteanime.com)

---

## 📸 Features

- User registration, login & profile management
- Thread creation with optional image upload
- Comments section under each thread
- Trending and Latest threads sections
- Highlighted comments
- Responsive design with Bootstrap 5 (Dark theme)
- Default avatars & thread images if none provided
- Admin panel for full control
- Animated sections & dynamic content

---

## 🛠️ Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/yourusername/liteanime.git
cd liteanime
```

### 2. Create virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Update `settings.py` with your MySQL config or use SQLite temporarily:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 5. Run migrations and collect static files

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

### 6. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

---

## 🗂️ Folder Structure

```
liteanime/
│
├── core/                  # Main app: views, models, forms, urls
├── templates/             # All HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded images
├── liteanime/             # Main project config
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Deployment (Production)

This project is deployable on platform:

- ✅ AWS EC2


Includes support for:

- `gunicorn` + `nginx`
- MySQL + Media file hosting
- HTTPS via Let's Encrypt

---

## 🔐 Security

This project follows Django’s built-in security standards and includes the following measures:

### ✅ CSRF Protection  
All forms include `{% csrf_token %}` to protect against Cross-Site Request Forgery (CSRF).  
Middleware is enabled by default via:

```python
'django.middleware.csrf.CsrfViewMiddleware',
```

---

### ✅ SQL Injection Protection  
All database operations are handled through Django ORM (`objects.create()`, `filter()`, etc.),  
which automatically escapes queries and protects against SQL injection.

---

### ✅ XSS Protection  
Django templates auto-escape user input (like `{{ comment.content }}`) to protect against  
Cross-Site Scripting (XSS) attacks.

---

### ✅ Form Validation  
- Custom validations are used in forms like `RegisterForm` (e.g. password confirmation check).
- Validation errors are clearly displayed to users.
- You can enhance further by adding field-specific validation (e.g. password strength, content checks).

---

> ✅ The platform is safe by design using Django’s security mechanisms.
> For extra hardening, features like rate-limiting and CAPTCHA can be added in the future.

---

## ❤️ Credits

Built with passion by Anas Obaid  
Feel free to contribute or report issues via GitHub.

---

## 📧 Contact

For collaboration, ideas, or support:  
📩 AnasObaid770@gmail.com