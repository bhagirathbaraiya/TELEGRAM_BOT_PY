from datetime import datetime
from ..firebase_config import initialize_firebase

async def counter(id_value, id_type):
    try:
        db = initialize_firebase()
        counter_ref = db.collection('counters').document(f"{id_type}_{id_value}")
        counter_doc = counter_ref.get()
        
        if counter_doc.exists:
            current_count = counter_doc.to_dict().get('count', 0)
            counter_ref.update({
                'count': current_count + 1,
                'last_used': datetime.now()
            })
        else:
            counter_ref.set({
                'id': id_value,
                'type': id_type,
                'count': 1,
                'created_at': datetime.now(),
                'last_used': datetime.now()
            })
        
    except Exception as e:
        print(f"Error updating counter: {e}")
