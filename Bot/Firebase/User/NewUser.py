from datetime import datetime
from ..firebase_config import initialize_firebase

async def new_user(chat_id, username, first_name, last_name):
    try:
        db = initialize_firebase()
        user_data = {
            'chat_id': chat_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'allowed': False,
            'created_at': datetime.now(),
        }
        db.collection('users').document(str(chat_id)).set(user_data)
    except Exception as e:
        print(f"Error adding new user: {e}")
