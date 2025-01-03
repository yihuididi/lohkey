# Project Lohkey #

This project uses Django as the backend framework to handle business logic and database interactions, while the frontend is built with basic HTML and CSS for simplicity.

_____________________________________________________________________________________________

## What Does This Project Use? ##

**• Backend:** Django

**• Frontend:** HTML and CSS
(Note: React or Vue.js is intentionally avoided for simplicity.)

_____________________________________________________________________________________________

## How Things Work Around Here? ##

1. Routers
   
	**• Routers:**
   	The two files "lohkey/lohkey/users/urls.py" and "lohkey/lohkey/users/views.py" are both used as routers


2. Templates
   
	**• Files Handling Templates:**
The templates (HTML files) are stored in the templates directory of each app. (e.g. lohkey/users/templates/home.html: This is the HTML file rendered by the home view.)

_____________________________________________________________________________________________

## Basic Commands ##

**1. Running the Server**
```bash
cd lohkey/lohkey
python3 manage.py runserver
```
Open your browser and go to http://127.0.0.1:8000.


**2. Downloading Packages into the Environment**
```bash
source .venv/bin/activate  # Activate the virtual environment
pip install package_name   # Install the package
deactivate                 # Deactivate the virtual environment (optional)
```

_____________________________________________________________________________________________















