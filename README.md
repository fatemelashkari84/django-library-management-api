# Library Management API

A RESTful API for managing a library, including books, authors, categories, user authentication with JWT, and book reviews.

## Features

- Book CRUD operations
- Author CRUD operations
- Category CRUD operations
- Filter books by title, author, and category
- Pagination for book lists
- JWT authentication using access and refresh tokens
- Retrieve the currently authenticated user's information
- Create, update, and delete reviews
- Prevent users from reviewing the same book more than once
- Restrict review updates and deletions to the review owner
- Serializer validation and appropriate HTTP status codes

## Technologies

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite (default database)
- Git

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd library
```

Replace `<repository-url>` with the actual repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/books/`

## Authentication

The API uses JSON Web Tokens (JWT).

### Obtain tokens

**POST** `/books/api/token/`

Request body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

The response contains an `access` token and a `refresh` token.

### Refresh an access token

**POST** `/books/api/token/refresh/`

Request body:

```json
{
  "refresh": "your_refresh_token"
}
```

Use the returned access token for authenticated requests.

### Get the current user

**GET** `/books/api/users/me/`

Requires authentication.

Header:

```http
Authorization: Bearer <access_token>
```

Returns information about the authenticated user.

## API Endpoints

All endpoints use the `/books/` prefix because the project's root URL configuration includes the `book` application's URLs under `books/`.

### Books

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/api/books/` | List books (paginated) |
| GET | `/books/api/books/<id>/` | Retrieve book details |
| POST | `/books/api/books/create/` | Create a book |
| PUT, PATCH | `/books/api/books/<id>/update/` | Update a book |
| DELETE | `/books/api/books/<id>/delete/` | Delete a book |
| GET | `/books/api/books/filter/` | Filter books |

Book filtering supports the following query parameters:

- `title`: filter by title
- `author`: filter by author ID
- `category`: filter by category ID

Example:

`GET /books/api/books/filter/?author=2`

Pagination supports `page` and `page_size` query parameters.

Example:

`GET /books/api/books/?page=1&page_size=5`

### Authors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/api/authors/` | List authors |
| GET | `/books/api/authors/<id>/` | Retrieve author details |
| POST | `/books/api/authors/create/` | Create an author |
| PUT, PATCH | `/books/api/authors/<id>/update/` | Update an author |
| DELETE | `/books/api/authors/<id>/delete/` | Delete an author |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/api/categories/` | List categories |
| GET | `/books/api/categories/<id>/` | Retrieve category details |
| POST | `/books/api/categories/create/` | Create a category |
| PUT, PATCH | `/books/api/categories/<id>/update/` | Update a category |
| DELETE | `/books/api/categories/<id>/delete/` | Delete a category |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/api/books/<id>/reviews/` | List reviews for a book |
| POST | `/books/api/reviews/create/` | Create a review |
| PUT, PATCH | `/books/api/reviews/<id>/update/` | Update a review |
| DELETE | `/books/api/reviews/<id>/delete/` | Delete a review |

Review creation requires authentication. The authenticated user is assigned automatically, and each user can review a particular book only once. Users may update or delete only their own reviews.

## Data Models

### Author

- `name`: author's name
- `bio`: optional biography
- `created_at`: creation timestamp

### Category

- `name`: unique category name

### Book

- `title`: book title
- `description`: optional description
- `published_year`: optional publication year
- `author`: many-to-many relationship with authors
- `category`: foreign key to a category
- `created_at`: creation timestamp
- `updated_at`: last update timestamp

A book can have multiple authors and belongs to one category.

### Review

- `book`: reviewed book
- `user`: user who wrote the review
- `rating`: numeric rating
- `comment`: optional comment
- `created_at`: creation timestamp

A database constraint prevents the same user from reviewing the same book more than once.

## Testing

Run all tests with:

```bash
python manage.py test
```

The test suite covers:

- Filtering books by author ID
- Filtering with a nonexistent author ID
- Rejecting unauthenticated book creation
- Preventing users from updating another user's review
- Preventing users from deleting another user's review
- Preventing duplicate reviews
- Current-user endpoint authentication and response

## HTTP Status Codes

Common response codes include:

- `200 OK`: successful retrieval or update
- `201 Created`: resource successfully created
- `204 No Content`: resource successfully deleted
- `400 Bad Request`: invalid request data
- `401 Unauthorized`: authentication is missing or invalid
- `403 Forbidden`: the user is not allowed to perform the operation
- `404 Not Found`: requested resource does not exist

## Notes

- Authenticated endpoints require a valid access token.
- Store tokens securely and do not commit credentials or secret keys to version control.
- For production deployment, configure appropriate `ALLOWED_HOSTS`, environment variables, database settings, and HTTPS.
