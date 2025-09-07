import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

async def block_user(user_id, username, first_name):
    try:
        if not firebase_admin._apps:
            pass
        
        db = firestore.client()
        user_ref = db.collection('users').document(str(user_id))
        user_ref.set({
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'allowed': False,
            'blocked_at': datetime.now()
        }, merge=True)
    except Exception as e:
        print(f"Error blocking user: {e}")
