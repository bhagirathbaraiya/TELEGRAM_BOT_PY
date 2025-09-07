from datetime import datetime
from ..firebase_config import initialize_firebase

async def counter(id_value, type_value):
    try:
        db = initialize_firebase()
        if db is None:
            print("Error updating counter: Firebase not initialized")
            return
        
        counter_ref = db.ref(f'MU_BOT/COUNTERS/{type_value}_{id_value}')
        snapshot = await counter_ref.get()
        
        if snapshot.exists:
            current_data = snapshot.val()
            count = current_data.get('count', 0) + 1
        else:
            count = 1
        
        counter_data = {
            'id': id_value,
            'type': type_value,
            'count': count,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        await counter_ref.set(counter_data)
    except Exception as e:
        print(f"Error updating counter: {e}")
