from ..firebase_config import initialize_firebase

async def check_id(id_value, type_value):
    try:
        db = initialize_firebase()
        if db is None:
            print("Error checking ID: Firebase not initialized")
            return True
        
        snapshot = await db.ref(f'MU_BOT/BLOCKED_IDS/{type_value}_{id_value}').get()
        if snapshot.exists:
            return False
        return True
    except Exception as e:
        print(f"Error checking ID: {e}")
        return True
