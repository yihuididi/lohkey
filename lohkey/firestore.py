import os
from firebase_admin import credentials, firestore
import firebase_admin

# Dynamically determine the absolute path to the credentials file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "lohkey-91b0d-firebase-adminsdk-32057-d38d9d22b2.json")

# Print the absolute path for debugging
print("Using credentials file at:", cred_path)

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("Firebase app initialized.")

# Firestore client
db = firestore.client()