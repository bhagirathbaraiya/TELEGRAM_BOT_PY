from ..firebase_config import initialize_firebase

async def get_bot_data():
    try:
        db = initialize_firebase()
        bot_ref = db.collection('bot_config').document('settings')
        bot_doc = bot_ref.get()
        
        if bot_doc.exists:
            return bot_doc.to_dict()
        
        return {}
        
    except Exception as e:
        print(f"Error getting bot data: {e}")
        return {}
