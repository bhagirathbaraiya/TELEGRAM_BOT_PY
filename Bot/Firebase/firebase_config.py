import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FirebaseDatabase:
    def __init__(self):
        self.data = {
            'MU_BOT': {
                'USERS': {},
                'LOGS': {},
                'COUNTERS': {},
                'MESSAGES': {},
                'IMAGES': {},
                'BOT_STATUS': {'active': True},
                'BLOCKED_IDS': {},
                'ALLOWED_IDS': {}
            }
        }
    
    def ref(self, path):
        return FirebaseRef(self.data, path)

class FirebaseRef:
    def __init__(self, data, path):
        self.data = data
        self.path = path
        self.path_parts = path.split('/')
    
    async def set(self, value):
        current = self.data
        for part in self.path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[self.path_parts[-1]] = value
        print(f"Firebase SET {self.path}: {value}")
    
    async def update(self, value):
        current = self.data
        for part in self.path_parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if self.path_parts[-1] not in current:
            current[self.path_parts[-1]] = {}
        
        if isinstance(current[self.path_parts[-1]], dict) and isinstance(value, dict):
            current[self.path_parts[-1]].update(value)
        else:
            current[self.path_parts[-1]] = value
        print(f"Firebase UPDATE {self.path}: {value}")
    
    async def get(self):
        current = self.data
        try:
            for part in self.path_parts:
                current = current[part]
            return FirebaseSnapshot(current, True)
        except (KeyError, TypeError):
            return FirebaseSnapshot(None, False)

class FirebaseSnapshot:
    def __init__(self, data, exists):
        self._data = data
        self.exists = exists
    
    def val(self):
        return self._data

def initialize_firebase():
    return FirebaseDatabase()

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
