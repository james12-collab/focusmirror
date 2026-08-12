from firebase_db import db
import json

def export_all_sessions():
    """Pull every session from every user's subcollection"""
    all_sessions = []
    users = db.collection('users').stream()
    
    for user_doc in users:
        username = user_doc.id
        sessions = db.collection('users').document(username).collection('sessions').stream()
        for s in sessions:
            data = s.to_dict()
            data.pop('created_at', None)  # not JSON serializable
            data['username'] = username
            all_sessions.append(data)
    
    print(f"Exported {len(all_sessions)} real sessions")
    with open('training_data_raw.json', 'w') as f:
        json.dump(all_sessions, f, indent=2)

if __name__ == '__main__':
    export_all_sessions()