# Project Lohkey #

This project uses Django as the backend framework to handle business logic and database interactions, while the frontend is built with basic HTML and CSS for simplicity.

_____________________________________________________________________________________________

## What Does This Project Use? ##

**• Backend:** Django

**• Frontend:** HTML and CSS
(Note: React or Vue.js is intentionally avoided for simplicity.)

_____________________________________________________________________________________________

## How Things Work Around Here? ##

**1. Routers**
   
   • The two files "lohkey/lohkey/users/urls.py" and "lohkey/lohkey/users/views.py" are both used as routers


**2. Templates**
   
   • The templates (HTML files) are stored in the templates directory of each app. (e.g. lohkey/users/templates/home.html: This is the HTML file rendered by the home view.)

_____________________________________________________________________________________________

## Basic Commands ##

**1. Clone to your desired directory 'github.com/ChounRH/lohkey'**

**2. Downloading Packages into the Environment**
```bash
source .venv/bin/activate  # Activate the virtual environment
pip install package_name   # Install all required packages (see requirements.txt)
deactivate                 # Deactivate the virtual environment (optional)
```

**3. Running the Server**
```bash
cd lohkey/lohkey
python3 manage.py runserver
```
If there are any missing dependencies / libraries, terminal should prompt that they are missing and you can install them from there

Open your browser and go to http://127.0.0.1:8000.






_____________________________________________________________________________________________















