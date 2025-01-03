#Project Lohkey#

This project uses Django as the backend framework to handle business logic and database interactions, while the frontend is built with basic HTML and CSS for simplicity.

_____________________________________________________________________________________________

##What Does This Project Use?##

•	**Backend:** Django
•	**Frontend:** HTML and CSS
(Note: React or Vue.js is intentionally avoided for simplicity.)

_____________________________________________________________________________________________

##How Things Work Around Here?##

1. Routers
   
**•	Files Handling Routers:**
The routing logic for this project is defined in the following files:

	•	urls.py: This file is where URL patterns are defined. Each URL is mapped to a corresponding view function in the views.py file.
	  •	Example:
	    •	lohkey/urls.py defines project-level routing.
	    •	App-specific routing is defined in app directories (e.g., users/urls.py).

2. Templates
   
**•	Files Handling Templates:**
The templates (HTML files) are stored in the templates directory of each app.
	•	Example:
	  •	lohkey/users/templates/home.html: This is the HTML file rendered by the home view.
	  •	Template Directory Configuration: The DIRS setting in settings.py ensures Django can locate these templates.

_____________________________________________________________________________________________

##Basic Commands##

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















