from ..firebase_config import initialize_firebase

async def check_user(user_id):
    try:
        db = initialize_firebase()
        if db is None:
            return False
        
        snapshot = await db.ref(f'MU_BOT/USERS/{user_id}').get()
        if snapshot.exists:
            user = snapshot.val()
            status = user.get('data', {})
            return status.get('status') == 'allowed'
        return False
    except Exception as e:
        print(f"Error checking user: {e}")
        return False
