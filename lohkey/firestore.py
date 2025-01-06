import os
from firebase_admin import credentials, firestore
import firebase_admin

# Dynamically determine the absolute path to the credentials file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "lohkey-91b0d-firebase-adminsdk-32057-3cd75b4f75.json")

# Print the absolute path for debugging
print("Using credentials file at:", cred_path)

# Use the credentials
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    'task': 'wash the dishes',
}

doc_ref = db.collection('taskscollection').document()
doc_ref.set(data)