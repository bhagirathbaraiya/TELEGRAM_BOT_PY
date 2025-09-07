import os
from dotenv import load_dotenv

load_dotenv()

class MockFirestore:
    def collection(self, name):
        return MockCollection()
    
class MockCollection:
    def document(self, doc_id):
        return MockDocument()
    
    def add(self, data):
        return MockDocument()

class MockDocument:
    def get(self):
        return MockDocumentSnapshot()
    
    def set(self, data, merge=False):
        pass
    
    def update(self, data):
        pass

class MockDocumentSnapshot:
    def __init__(self):
        self.exists = True
    
    def to_dict(self):
        return {
            'allowed': True,
            'active': True,
            'count': 1
        }

def initialize_firebase():
    return MockFirestore()

def get_firebase_config():
    return {
        'apiKey': os.getenv('FIREBASE_API_KEY'),
        'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
        'projectId': os.getenv('FIREBASE_PROJECT_ID'),
        'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.getenv('FIREBASE_APP_ID')
    }
