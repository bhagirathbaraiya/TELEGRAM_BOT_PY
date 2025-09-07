from ..firebase_config import initialize_firebase

async def check_id(id_value, id_type):
    try:
        db = initialize_firebase()
        collection_name = f"{id_type}_ids"
        id_ref = db.collection(collection_name).document(str(id_value))
        id_doc = id_ref.get()
        
        if id_doc.exists:
            id_data = id_doc.to_dict()
            return id_data.get('allowed', False)
        
        return False
        
    except Exception as e:
        print(f"Error checking ID: {e}")
        return False
