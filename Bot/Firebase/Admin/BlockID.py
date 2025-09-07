from datetime import datetime
from ..firebase_config import initialize_firebase

async def block_id(id_value, id_type="student"):
    try:
        db = initialize_firebase()
        collection_name = f"{id_type}_ids"
        id_ref = db.collection(collection_name).document(str(id_value))
        id_ref.set({
            'id': id_value,
            'allowed': False,
            'blocked_at': datetime.now(),
            'type': id_type
        })
    except Exception as e:
        print(f"Error blocking ID: {e}")
