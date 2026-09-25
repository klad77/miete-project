# Miete Project

Miete is a Django REST API for managing rental housing. It supports users, property listings, bookings, availability checks, ratings, reviews, search history, and basic analytics.

## Features

- User registration and JWT authentication
- JWT access and refresh tokens in HttpOnly cookies
- Property listing management
- Owner-only listing updates and deletion
- Search, filtering, and sorting
- Booking overlap validation
- Booking confirmation and rejection by property owners
- Booking cancellation rules
- Available-date calculation
- Ratings and reviews after completed bookings
- One rating per completed booking
- Search and advertisement view history
- Popular searches and advertisements
- Swagger and ReDoc documentation
- Automated API and permission tests
- Docker Compose environment with Django and MySQL

## Technology Stack

- Python 3.12
- Django 5.1
- Django REST Framework 3.15
- Simple JWT
- django-filter
- drf-spectacular
- OpenAPI 3
- SQLite
- MySQL 8.4
- Docker and Docker Compose

## Project Structure

```text
miete-project/
├── apps/
│   ├── apartments/
│   ├── bookings/
│   └── users/
├── miete/
│   ├── settings.py
│   └── urls.py
├── .dockerignore
├── compose.yaml
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
```

## Running with Docker

Docker Compose starts two services:

- `web` — Django development server;
- `db` — MySQL database.

Build the Django image:

```powershell
docker compose build
```

Start the containers:

```powershell
docker compose up -d
```

Check their status:

```powershell
docker compose ps
```

The MySQL container should have the `healthy` status, and the Django container should have the `Up` status.

Open the application:

```text
http://127.0.0.1:8000/
```

Swagger documentation:

```text
http://127.0.0.1:8000/api/swagger/
```

ReDoc documentation:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI 3 schema:

```text
http://127.0.0.1:8000/api/schema/
```

View Django logs:

```powershell
docker compose logs -f web
```

Run Django system checks:

```powershell
docker compose exec web python manage.py check
```

Create a superuser in the container:

```powershell
docker compose exec web python manage.py createsuperuser
```

Run all automated tests inside the container:

```powershell
docker compose exec -e MYSQL=False web python manage.py test
```

Stop the containers while preserving the MySQL data:

```powershell
docker compose down
```

To delete the containers and the local MySQL volume:

```powershell
docker compose down -v
```

Warning: `docker compose down -v` permanently deletes the MySQL data stored in the Docker volume.

The default passwords in `compose.yaml` are intended only for local development. Production credentials must be supplied through secure environment variables.

## Local Installation without Docker

### 1. Clone the repository

```powershell
git clone git@github.com:klad77/miete-project.git
cd miete-project
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create `.env`

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-your-own-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

MYSQL=False
```

The `.env` file contains secrets and must not be committed to Git.

### 5. Apply migrations

```powershell
python manage.py migrate
```

### 6. Create an administrator

```powershell
python manage.py createsuperuser
```

### 7. Start the server

```powershell
python manage.py runserver
```

## Database Configuration

### SQLite

SQLite is recommended for simple local development:

```env
MYSQL=False
```

Django will use the local `db.sqlite3` file.

### MySQL

To use an existing MySQL server without Docker:

```env
MYSQL=True
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306
```

The Docker Compose environment overrides these settings for its containers and connects Django to the `db` service.

## Main API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/register/` | Register a user |
| POST | `/api/users/login/` | Log in and set JWT cookies |
| POST | `/api/users/logout/` | Remove JWT cookies |
| GET | `/api/users/protected/` | Test authenticated access |
| POST | `/api/users/token/` | Obtain a JWT token pair |
| POST | `/api/users/token/refresh/` | Refresh an access token |

### Advertisements

| Method | Endpoint | Description |
|---|---|---|
| GET, POST | `/api/apartments/advertisements/` | List or create advertisements |
| GET | `/api/apartments/advertisements/search/` | Search and filter advertisements |
| GET, PATCH, DELETE | `/api/apartments/advertisements/{id}/` | Retrieve or manage an advertisement |
| POST | `/api/apartments/advertisements/{id}/status/` | Toggle advertisement status |
| GET | `/api/apartments/advertisements/{id}/reviews/` | List ratings and reviews |
| POST | `/api/apartments/advertisements/{id}/add-review/` | Add a rating and review |
| GET | `/api/apartments/advertisement/{id}/available-dates/` | Get available dates |
| GET | `/api/apartments/advertisements/popular/` | List popular advertisements |
| GET | `/api/apartments/advertisements/views/` | Get the user's view history |
| GET | `/api/apartments/search-history/` | Get the user's search history |
| GET | `/api/apartments/search/popular/` | List popular searches |

### Bookings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings/bookings/` | Create a booking |
| GET | `/api/bookings/bookings/{id}/` | Retrieve the user's booking |
| GET | `/api/bookings/bookings/user/` | List the current user's bookings |
| GET | `/api/bookings/bookings/owner/` | List bookings for the owner's listings |
| PATCH | `/api/bookings/bookings/{id}/cancel/` | Cancel a booking |
| PATCH | `/api/bookings/bookings/{id}/owner-status/` | Confirm or reject a booking |

Booking lists support status filtering:

```text
/api/bookings/bookings/user/?status=pending
/api/bookings/bookings/owner/?status=confirmed
```

## Booking and Rating Rules

- The start date cannot be in the past.
- The end date must be later than the start date.
- Pending and confirmed bookings block occupied dates.
- A checkout date can be used as the next check-in date.
- A booking can be canceled at least two days before check-in.
- Only a property owner can confirm or reject a pending booking.
- A rating can be added only after a completed booking.
- One completed booking can receive only one rating.

## Authentication

Registration and login create JWT access and refresh tokens stored in HttpOnly cookies.

Protected endpoints also support the standard header:

```text
Authorization: Bearer <access_token>
```

The local development environment uses:

```text
Secure=False
SameSite=Lax
```

Production deployments must use HTTPS and secure cookies.

## Tests

Run all tests locally:

```powershell
python manage.py test
```

Run all tests inside Docker:

```powershell
docker compose exec -e MYSQL=False web python manage.py test
```

The current suite contains 61 automated tests covering:

- registration and authentication;
- JWT cookies;
- advertisement permissions;
- search and filtering;
- booking overlap validation;
- cancellation rules;
- owner status management;
- available dates;
- ratings and reviews;
- search and view history;
- booking lists and object-level permissions.

Check for missing migrations:

```powershell
python manage.py makemigrations --check --dry-run
```

Run Django checks:

```powershell
python manage.py check
```

Validate the OpenAPI 3 schema:

```powershell
python manage.py spectacular --file schema.yml --validate
```

## Security Notes

- Never commit `.env`.
- Never commit `db.sqlite3`.
- Never commit private SSH keys.
- Use a new secret key in production.
- Set `DEBUG=False` in production.
- Configure appropriate `ALLOWED_HOSTS`.
- Use HTTPS and secure cookies in production.
- Replace all Docker development passwords before production use.
