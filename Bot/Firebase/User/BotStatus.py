from ..firebase_config import initialize_firebase

async def get_bot_status():
    try:
        db = initialize_firebase()
        if db is None:
            return True
        
        snapshot = await db.ref('MU_BOT/BOT_STATUS').get()
        if snapshot.exists:
            status_data = snapshot.val()
            return status_data.get('active', True)
        return True
    except Exception as e:
        print(f"Error getting bot status: {e}")
        return True
