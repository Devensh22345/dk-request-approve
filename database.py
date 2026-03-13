from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']
messages = client['main']['messages']  # New collection for storing messages

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id):
    in_db = already_dbg(chat_id)
    if in_db:
        return
    return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

# New functions for message storage
def save_message(message_data):
    """Save a message to database"""
    try:
        # Check if message already exists
        existing = messages.find_one({"message_id": message_data["message_id"]})
        if existing:
            return existing
        
        # Insert new message
        messages.insert_one(message_data)
        return message_data
    except Exception as e:
        print(f"Error saving message: {e}")
        return None

def get_all_messages():
    """Get all stored messages"""
    try:
        return list(messages.find({}))
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []

def clear_messages():
    """Clear all stored messages (for testing)"""
    try:
        messages.delete_many({})
        return True
    except Exception as e:
        print(f"Error clearing messages: {e}")
        return False

def count_messages():
    """Count total stored messages"""
    try:
        return messages.count_documents({})
    except Exception as e:
        print(f"Error counting messages: {e}")
        return 0
