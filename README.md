# LiteAnime 🎌

**LiteAnime** is a social platform for anime, manga, and novel lovers. Built with Django, Bootstrap, and custom CSS/JS, the platform offers a dynamic space for users to interact, create threads, comment, and explore community content.

---

## 🔧 Features

- User registration and login system
- User profile with editable info and avatar upload
- Create, view, and comment on threads
- Thread images (with fallback to default)
- Trending threads (based on views)
- Latest threads (based on creation date)
- Highlighted comments (based on reactions)
- Responsive UI with Bootstrap 5
- Dark mode theme with modern design
- Navigation bar with profile logic and dropdown menu
- About Us and Contact Us pages
- Footer with social icons and scroll-to-top functionality
- Admin panel for content moderation

---

## 💻 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite / MySQL (recommended for production)
- **Media**: File/image uploads handled by Django
- **Deployment**: AWS EC2 (Linux), Gunicorn, Nginx
- **Version Control**: Git & GitHub

---

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/xAnoOos/liteanime.git
   cd liteanime
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit:
   ```
   http://127.0.0.1:8000/
   ```

---

## 📁 Project Structure

```
liteanime/
├── core/               # Main Django app (threads, profiles, comments)
│   ├── models.py       # Models for UserProfile, Thread, Comment, etc.
│   ├── views.py        # Views for rendering and logic
│   ├── forms.py        # Forms for thread creation, profile editing
│   ├── urls.py         # App URLs
│   ├── templates/      # HTML Templates
│   └── static/         # CSS, JS, and images
├── liteanime/          # Project settings and URLs
├── media/              # Uploaded media files
├── manage.py
├── requirements.txt
└── README.md
```

---

## 📝 Notes

- Make sure to configure `MEDIA_URL` and `MEDIA_ROOT` in `settings.py` for file uploads.
- Static files should be collected for production using:
  ```bash
  python manage.py collectstatic
  ```

---

## 🙌 Credits

Built by **Anas Obaid**  

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
