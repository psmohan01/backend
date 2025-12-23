Django backend for Cal Booking project.
- Install: pip install -r requirements.txt
- Copy .env.example to .env and fill values.
- Run migrations: python manage.py migrate
- Start server: python manage.py runserver 8000
Endpoints:
- GET /api/availability/?date=YYYY-MM-DD
- POST /api/create/  (body: name, email, startISO, endISO, notes, display)
