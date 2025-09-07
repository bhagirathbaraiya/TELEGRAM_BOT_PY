from ..firebase_config import initialize_firebase

async def get_bot_status():
    try:
        db = initialize_firebase()
        status_ref = db.collection('bot_config').document('status')
        status_doc = status_ref.get()
        
        if status_doc.exists:
            status_data = status_doc.to_dict()
            return status_data.get('active', True)
        
        return True
        
    except Exception as e:
        print(f"Error getting bot status: {e}")
        return True
