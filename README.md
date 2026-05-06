# Tribu

A cyberpunk-themed blog platform built with Django. Users can write posts, manage their profile and browse content from other members of the community.

## Features

- **Authentication** — sign up, log in and log out
- **Posts** — create, read, edit and delete posts; only the author can modify their own
- **User profiles** — public profile page with bio, avatar and a list of the user's posts
- **Unique slugs** — post slugs are generated automatically from the title and deduplicated

## Project structure

```
Blog/
├── accounts/   # Authentication (login, logout, signup)
├── posts/      # Post CRUD
├── users/      # User profiles
├── shared/     # Base templates, static files (CSS, images), shared decorators
└── main/       # Django project settings and root URLs
```

## Setup

The project uses [uv](https://github.com/astral-sh/uv) as the package manager and [just](https://github.com/casey/just) as the task runner.

```bash
# Install dependencies and run initial migrations
just setup

# Start the development server (default port 8000)
just dev

# Start with external network access
just dev0
```

If you don't have `just`, you can use the venv directly:

```bash
uv sync
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

## Common commands

| Command | Description |
|---|---|
| `just dev` | Start development server |
| `just mm` | Create migrations (`makemigrations`) |
| `just m` | Apply migrations (`migrate`) |
| `just c` | Run Django system check |
| `just sh` | Open Django shell |
| `just create-su` | Create or update superuser (`admin`/`admin`) |
| `just create-user <username> <password> <email>` | Create a regular user |
| `just reset-db` | Drop database and migrations and start fresh |
| `just test` | Run test suite |

## URL map

| URL | View | Description |
|---|---|---|
| `/` | index | Redirect to post list |
| `/login/` | `accounts:login` | Log in |
| `/signup/` | `accounts:signup` | Create account |
| `/logout/` | `accounts:logout` | Log out |
| `/posts/` | `posts:post-list` | All posts |
| `/posts/add/` | `posts:post-add` | New post (login required) |
| `/posts/<slug>/` | `posts:post-detail` | Post detail |
| `/posts/<slug>/edit` | `posts:post-edit` | Edit post (author only) |
| `/posts/<slug>/delete` | `posts:post-delete` | Delete post (author only) |
| `/users/<username>/` | `users:profile-detail` | User profile |
| `/users/edit/` | `users:profile-edit` | Edit own profile (login required) |

## Tech stack

- **Backend** — Django 6
- **Database** — SQLite (development)
- **Images** — Pillow (avatar uploads)
- **Package manager** — uv
- **Task runner** — just
