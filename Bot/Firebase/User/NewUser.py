from datetime import datetime
from ..firebase_config import initialize_firebase

async def new_user(user_id, username, first_name, last_name):
    try:
        db = initialize_firebase()
        if db is None:
            return
        
        user_data = {
            'data': {
                'userID': str(user_id),
                'username': username or '',
                'firstName': first_name or '',
                'lastName': last_name or '',
                'status': 'blocked',
                'joinedDate': datetime.now().strftime('%m/%d/%Y')
            }
        }
        
        await db.ref(f'MU_BOT/USERS/{user_id}').set(user_data)
    except Exception as e:
        print(f"Error adding new user: {e}")
