from datetime import datetime
from ..firebase_config import initialize_firebase

async def write_user_log(message, log_type="info"):
    try:
        db = initialize_firebase()
        log_data = {
            'message': message,
            'type': log_type,
            'timestamp': datetime.now(),
        }
        db.collection('user_logs').add(log_data)
    except Exception as e:
        print(f"Error writing log: {e}")
