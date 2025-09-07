import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

async def allow_id(id_value, id_type="student"):
    try:
        if not firebase_admin._apps:
            pass
        
        db = firestore.client()
        collection_name = f"{id_type}_ids"
        id_ref = db.collection(collection_name).document(str(id_value))
        id_ref.set({
            'id': id_value,
            'allowed': True,
            'allowed_at': datetime.now(),
            'type': id_type
        })
    except Exception as e:
        print(f"Error allowing ID: {e}")
