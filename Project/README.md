# Project Instructions

## Prerequisites

### Install Latest Python

Download and install Python from: https://www.python.org/downloads/

---

# Steps to Follow

## Open a Terminal

-   **Windows:** Use `cmd`
-   **Linux/MacOS:** Use `shell`

## Enter the Following Commands

### For Windows:

```bash
pip install virtualenv
virtualenv django-env
django-env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py clearsessions
python manage.py runserver
```

### For Linux/MacOS:

```bash
pip3 install virtualenv
virtualenv django-env
source django-env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py clearsessions
python3 manage.py runserver
```

## Open a Web Browser and Enter:

```
http://localhost:8000
```
