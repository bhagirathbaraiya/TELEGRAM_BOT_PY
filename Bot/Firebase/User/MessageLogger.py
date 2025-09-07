import re
import time
import asyncio
from datetime import datetime
from ..firebase_config import initialize_firebase

MAX_RETRIES = 3
RETRY_DELAY = 1.0

async def retry_operation(operation, retries=MAX_RETRIES):
    for i in range(retries):
        try:
            result = operation()
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception as error:
            if i == retries - 1:
                raise error
            print(f"Retry {i + 1} failed, retrying in {RETRY_DELAY}s...")
            await asyncio.sleep(RETRY_DELAY)

async def message_logger(telegram_user_id, message_text):
    try:
        db = initialize_firebase()
        if db is None:
            print("Error logging message: Firebase not initialized")
            return {'success': False, 'message': 'Firebase not initialized'}
        
        # Extract GR/ER number from message text
        gr_no_match = re.search(r'/grno\s*(\d+)', message_text, re.IGNORECASE)
        er_no_match = re.search(r'/erno\s*(\d+)', message_text, re.IGNORECASE)
        
        # Determine message type based on content
        message_type = 'other'
        message_status = 'pending'
        
        if '/erno' in message_text.lower():
            message_type = 'faculty'
        elif '/grno' in message_text.lower():
            message_type = 'student'
        
        # Check if this is a success/failure update for an existing message
        is_status_update = any(keyword in message_text.lower() for keyword in 
                              ['success', 'failed', 'sent successfully', 'error'])
        
        if is_status_update:
            # Get all messages and find the most recent pending one for this user
            messages_ref = db.ref('MU_BOT/MESSAGES')
            snapshot = await messages_ref.get()
            
            if snapshot.exists:
                messages = snapshot.val()
                last_pending_message = None
                last_pending_key = None
                
                # Find the most recent pending message for this user
                for key, message in messages.items():
                    if (message.get('user_id') == telegram_user_id and 
                        message.get('message_status') == 'pending'):
                        last_pending_message = message
                        last_pending_key = key
                
                if last_pending_message:
                    # Update status based on message content
                    if any(keyword in message_text.lower() for keyword in ['success', 'sent successfully']):
                        message_status = 'success'
                        if er_no_match:
                            message_text = f"Successfully fetched ER image: {er_no_match.group(1)}"
                    elif any(keyword in message_text.lower() for keyword in ['error', 'failed']):
                        message_status = 'failed'
                    
                    # Update the existing message
                    updated_message = {
                        **last_pending_message,
                        'message_status': message_status,
                        'message_text': message_text
                    }
                    
                    await db.ref(f'MU_BOT/MESSAGES/{last_pending_key}').set(updated_message)
                    
                    return {
                        'success': True,
                        'message': 'Message status updated successfully',
                        'messageType': last_pending_message.get('message_type'),
                        'messageStatus': message_status,
                        'grNo': last_pending_message.get('grno'),
                        'erNo': er_no_match.group(1) if er_no_match else None
                    }
        
        # If not a status update or no pending message found, create new message
        timestamp = datetime.now().isoformat()
        message_id = str(int(time.time() * 1000))
        
        new_message = {
            'user_id': telegram_user_id,
            'grno': int(gr_no_match.group(1)) if gr_no_match else None,
            'message_type': message_type,
            'message_text': message_text,
            'message_status': message_status,
            'time_stamp': timestamp
        }
        
        await db.ref(f'MU_BOT/MESSAGES/{message_id}').set(new_message)
        
        # If it's a student message with GR number, update image counter
        if message_type == 'student' and gr_no_match:
            gr_no = int(gr_no_match.group(1))
            image_ref = db.ref(f'MU_BOT/IMAGES/student{gr_no}')
            
            image_snapshot = await image_ref.get()
            
            if image_snapshot.exists:
                current_data = image_snapshot.val()
                new_counter = current_data.get('counter', 0) + 1
                
                updated_image_data = {
                    **current_data,
                    'counter': new_counter
                }
                await image_ref.set(updated_image_data)
            else:
                # Create new image entry if it doesn't exist
                new_image_data = {
                    'counter': 1,
                    'status': 'allowed'
                }
                await image_ref.set(new_image_data)
        
        return {
            'success': True,
            'message': 'Message logged successfully',
            'messageType': message_type,
            'messageStatus': message_status,
            'grNo': int(gr_no_match.group(1)) if gr_no_match else None,
            'erNo': er_no_match.group(1) if er_no_match else None
        }
        
    except Exception as error:
        print(f'Error logging message: {error}')
        return {
            'success': False,
            'message': 'Failed to log message',
            'error': str(error)
        }
