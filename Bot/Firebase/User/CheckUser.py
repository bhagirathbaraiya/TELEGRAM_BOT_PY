from ..firebase_config import initialize_firebase

async def check_user(user_id):
    try:
        db = initialize_firebase()
        user_ref = db.collection('users').document(str(user_id))
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return user_data.get('allowed', False)
        
        return False
        
    except Exception as e:
        print(f"Error checking user: {e}")
        return False
