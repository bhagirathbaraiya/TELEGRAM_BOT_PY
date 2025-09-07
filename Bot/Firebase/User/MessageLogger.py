from datetime import datetime
from ..firebase_config import initialize_firebase

async def message_logger(user_id, message):
    try:
        db = initialize_firebase()
        log_data = {
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.now(),
        }
        db.collection('message_logs').add(log_data)
    except Exception as e:
        print(f"Error logging message: {e}")
