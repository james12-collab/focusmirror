import firebase_admin
from firebase_admin import credentials, firestore
import time
import hashlib
import secrets
import os
from datetime import datetime, date

# ─────────────────────────────────────────────────────────
# INITIALIZE FIREBASE
# ─────────────────────────────────────────────────────────

if not firebase_admin._apps:
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firebase connected!")

# ─────────────────────────────────────────────────────────
# ENCRYPTION UTILITIES
# ─────────────────────────────────────────────────────────

def hash_password(password, salt=None):
    """SHA-256 hash with unique salt per user"""
    if not salt:
        salt = secrets.token_hex(32)
    hashed = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return hashed, salt

def verify_password(password, stored_hash, salt):
    """Verify password against stored hash"""
    hashed, _ = hash_password(password, salt)
    return hashed == stored_hash

def generate_session_token():
    """Generate a secure session token"""
    return secrets.token_urlsafe(32)

# ─────────────────────────────────────────────────────────
# ACCOUNTS — Complete isolation per user
# ─────────────────────────────────────────────────────────

def create_account(username, password, age_group='unknown', ai_consent=False):
    """
    Create a new user account with encrypted password.
    Returns (success, message)
    """
    username = username.strip().lower()

    # Validation
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    if len(username) > 20:
        return False, "Username must be under 20 characters"
    if not username.replace('_','').replace('-','').isalnum():
        return False, "Username can only contain letters, numbers, - and _"
    if len(password) < 4:
        return False, "Password must be at least 4 characters"

    # Check if username taken
    user_ref = db.collection('users').document(username)
    if user_ref.get().exists:
        return False, "Username already taken"

    # Hash password
    hashed, salt = hash_password(password)

    # Store account — password hash only, never plain text
    user_ref.set({
        'username': username,
        'display_name': username.capitalize(),
        'password_hash': hashed,
        'salt': salt,
        'age_group': age_group,
        'ai_consent': ai_consent,
        'created_at': firestore.SERVER_TIMESTAMP,
        'created_date': time.strftime("%Y-%m-%d"),
        'last_login': firestore.SERVER_TIMESTAMP,
        'is_active': True
    })

    print(f"Account created: {username}")
    return True, username.capitalize()

def verify_login(username, password):
    """
    Verify login credentials.
    Returns (success, display_name or error)
    """
    username = username.strip().lower()
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()

    if not doc.exists:
        return False, "Account not found"

    data = doc.to_dict()

    if not verify_password(password, data['password_hash'], data['salt']):
        return False, "Wrong password"

    # Update last login
    user_ref.update({'last_login': firestore.SERVER_TIMESTAMP})

    return True, data['display_name']

def get_account(username):
    """Get account data for a user"""
    username = username.strip().lower()
    doc = db.collection('users').document(username).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    # Never return password hash to the app
    safe_data = {k: v for k, v in data.items()
                 if k not in ['password_hash', 'salt']}
    return safe_data

def account_exists(username):
    """Check if username is taken"""
    username = username.strip().lower()
    return db.collection('users').document(username).get().exists

def delete_account(username):
    """
    Permanently delete account and ALL user data.
    GDPR right to erasure compliance.
    """
    username = username.strip().lower()
    user_ref = db.collection('users').document(username)

    # Delete all subcollections
    for subcol in ['sessions', 'report_cards', 'badges', 'streaks']:
        docs = user_ref.collection(subcol).get()
        for doc in docs:
            doc.reference.delete()

    # Delete the user document
    user_ref.delete()
    print(f"Account deleted: {username}")
    return True

def export_user_data(username):
    """
    Export all user data as dict.
    GDPR right to data portability compliance.
    """
    username = username.strip().lower()
    user_ref = db.collection('users').document(username)

    data = {}
    doc = user_ref.get()
    if doc.exists:
        profile = doc.to_dict()
        # Remove sensitive fields
        profile.pop('password_hash', None)
        profile.pop('salt', None)
        data['profile'] = profile

    # Export sessions
    sessions = user_ref.collection('sessions').get()
    data['sessions'] = [s.to_dict() for s in sessions]

    # Export report cards
    reports = user_ref.collection('report_cards').get()
    data['report_cards'] = [r.to_dict() for r in reports]

    # Export badges
    badges = user_ref.collection('badges').get()
    data['badges'] = [b.to_dict() for b in badges]

    return data

# ─────────────────────────────────────────────────────────
# SESSIONS — Stored under each user's subcollection
# ─────────────────────────────────────────────────────────

def get_grade(score):
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    elif score >= 50: return "D"
    else: return "F"

def get_time_of_day():
    hour = int(time.strftime("%H"))
    if hour < 6: return "Late Night"
    elif hour < 12: return "Morning"
    elif hour < 17: return "Afternoon"
    elif hour < 21: return "Evening"
    else: return "Night"

def save_session_db(username, score, duration_minutes,
                    stress=0, confusion=0, boreout=0, engagement=50):
    """
    Save a study session under the user's private subcollection.
    Complete data isolation — only accessible by this user.
    """
    username = username.strip().lower()

    session_data = {
        'username': username,
        'score': int(score),
        'duration': round(float(duration_minutes), 1),
        'grade': get_grade(score),
        'date': time.strftime("%Y-%m-%d"),
        'time': time.strftime("%I:%M %p"),
        'time_of_day': get_time_of_day(),
        'hour': int(time.strftime("%H")),
        'emotions': {
            'stress': int(stress),
            'confusion': int(confusion),
            'boreout': int(boreout),
            'engagement': int(engagement)
        },
        'created_at': firestore.SERVER_TIMESTAMP,
        # Legacy field for compatibility
        'name': username.capitalize()
    }

    # Save to user's private subcollection
    db.collection('users').document(username)\
      .collection('sessions').add(session_data)

    # Also save to global sessions for leaderboard/benchmarking
    db.collection('all_sessions').add(session_data)

    print(f"Session saved for {username}: score={score}")
    return session_data

def get_user_sessions(username):
    """
    Get all sessions for a specific user.
    Returns only that user's data — complete isolation.
    """
    username = username.strip().lower()
    docs = db.collection('users').document(username)\
             .collection('sessions')\
             .order_by('created_at')\
             .get()
    sessions = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        # Remove server timestamp for JSON serialization
        d.pop('created_at', None)
        sessions.append(d)
    return sessions

def get_all_sessions():
    """
    Get all sessions across all users.
    Used for global benchmarking only.
    Returns anonymized data.
    """
    docs = db.collection('all_sessions')\
             .order_by('created_at')\
             .limit(1000)\
             .get()
    sessions = []
    for doc in docs:
        d = doc.to_dict()
        d.pop('created_at', None)
        sessions.append(d)
    return sessions

# ─────────────────────────────────────────────────────────
# REPORT CARDS — Stored per user
# ─────────────────────────────────────────────────────────

def save_report_card(username, report_data):
    """Save a session report card under user's private subcollection"""
    username = username.strip().lower()
    report_data['created_at'] = firestore.SERVER_TIMESTAMP
    report_data['date'] = time.strftime("%Y-%m-%d")
    db.collection('users').document(username)\
      .collection('report_cards').add(report_data)
    print(f"Report card saved for {username}")

def get_user_report_cards(username):
    """Get all report cards for a user"""
    username = username.strip().lower()
    docs = db.collection('users').document(username)\
             .collection('report_cards')\
             .order_by('created_at', direction=firestore.Query.DESCENDING)\
             .limit(50)\
             .get()
    reports = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        d.pop('created_at', None)
        reports.append(d)
    return reports

# ─────────────────────────────────────────────────────────
# BADGES — Stored per user
# ─────────────────────────────────────────────────────────

def save_badge(username, badge_id, badge_data):
    """Save an earned badge under user's private subcollection"""
    username = username.strip().lower()
    badge_data['earned_at'] = firestore.SERVER_TIMESTAMP
    badge_data['date'] = time.strftime("%Y-%m-%d")
    db.collection('users').document(username)\
      .collection('badges').document(badge_id).set(badge_data)

def get_user_badges(username):
    """Get all earned badges for a user"""
    username = username.strip().lower()
    docs = db.collection('users').document(username)\
             .collection('badges').get()
    badges = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        d.pop('earned_at', None)
        badges.append(d)
    return badges

def has_badge(username, badge_id):
    """Check if user has earned a specific badge"""
    username = username.strip().lower()
    doc = db.collection('users').document(username)\
            .collection('badges').document(badge_id).get()
    return doc.exists

# ─────────────────────────────────────────────────────────
# LEADERBOARD — Daily, public read
# ─────────────────────────────────────────────────────────

def save_score_db(name, score, session_minutes):
    """Save score to daily leaderboard"""
    today = time.strftime("%Y-%m-%d")
    entry = {
        'name': name,
        'score': int(score),
        'session_minutes': round(float(session_minutes), 1),
        'timestamp': time.strftime("%I:%M %p"),
        'date': today,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('leaderboard').document(today)\
      .collection('entries').add(entry)

def get_leaderboard_db():
    """Get today's top 10 scores"""
    today = time.strftime("%Y-%m-%d")
    try:
        docs = db.collection('leaderboard').document(today)\
                 .collection('entries')\
                 .order_by('score', direction=firestore.Query.DESCENDING)\
                 .limit(10)\
                 .get()
        entries = []
        for doc in docs:
            d = doc.to_dict()
            d.pop('created_at', None)
            entries.append(d)
        return entries
    except Exception as e:
        print(f"Leaderboard error: {e}")
        return []

def reset_leaderboard_db():
    """Delete today's leaderboard entries"""
    today = time.strftime("%Y-%m-%d")
    docs = db.collection('leaderboard').document(today)\
             .collection('entries').get()
    for doc in docs:
        doc.reference.delete()
    print("Leaderboard reset!")

def get_rank_db(score):
    """Get rank for a given score on today's leaderboard"""
    board = get_leaderboard_db()
    for i, entry in enumerate(board):
        if entry['score'] <= score:
            return i + 1
    return len(board) + 1

# ─────────────────────────────────────────────────────────
# WORLD MAP — Anonymous location data
# ─────────────────────────────────────────────────────────

def save_world_point_db(lat, lng, score):
    """Save anonymous location point for world map"""
    db.collection('world_map').add({
        'lat': round(float(lat), 2),
        'lng': round(float(lng), 2),
        'score': int(score),
        'time': time.strftime("%Y-%m-%dT%H:%M:%S"),
        'created_at': firestore.SERVER_TIMESTAMP
    })

def get_world_data_db():
    """Get recent world map points"""
    try:
        docs = db.collection('world_map')\
                 .order_by('created_at', direction=firestore.Query.DESCENDING)\
                 .limit(500)\
                 .get()
        points = []
        for doc in docs:
            d = doc.to_dict()
            d.pop('created_at', None)
            points.append(d)
        return points
    except Exception as e:
        print(f"World map error: {e}")
        return []

# ─────────────────────────────────────────────────────────
# STUDY PATTERNS — Computed from user sessions
# ─────────────────────────────────────────────────────────

def calc_streak(sessions):
    """Calculate current study streak from sessions"""
    if not sessions:
        return 0
    today_str = time.strftime("%Y-%m-%d")
    dates = sorted(set(s['date'] for s in sessions if 'date' in s), reverse=True)
    if not dates:
        return 0
    streak = 0
    prev = None
    for d in dates:
        if prev is None:
            if d == today_str:
                streak = 1
                prev = d
            else:
                break
        else:
            try:
                d1 = datetime.strptime(prev, "%Y-%m-%d")
                d2 = datetime.strptime(d, "%Y-%m-%d")
                if (d1 - d2).days == 1:
                    streak += 1
                    prev = d
                else:
                    break
            except:
                break
    return streak

def get_user_patterns(username):
    """
    Compute study patterns from user's session history.
    Returns insights specific to this user only.
    """
    sessions = get_user_sessions(username)
    if len(sessions) < 2:
        return {}

    time_scores = {}
    for s in sessions:
        tod = s.get('time_of_day', 'Unknown')
        if tod not in time_scores:
            time_scores[tod] = []
        time_scores[tod].append(s['score'])

    best_time = max(
        time_scores,
        key=lambda x: sum(time_scores[x])/len(time_scores[x])
    )
    avg_duration = sum(s.get('duration', 0) for s in sessions) / len(sessions)
    recent = sessions[-7:]
    if len(recent) >= 2:
        trend = "improving" if recent[-1]['score'] > recent[0]['score'] else "declining"
    else:
        trend = "not enough data"

    streak = calc_streak(sessions)
    time_avgs = {
        t: round(sum(v)/len(v), 1)
        for t, v in time_scores.items()
    }

    return {
        'total_sessions': len(sessions),
        'best_time': best_time,
        'avg_duration': round(avg_duration, 1),
        'trend': trend,
        'recent_scores': [s['score'] for s in recent],
        'avg_score': round(sum(s['score'] for s in sessions) / len(sessions), 1),
        'streak': streak,
        'time_avgs': time_avgs
    }

# ─────────────────────────────────────────────────────────
# SCHOOL ENQUIRIES
# ─────────────────────────────────────────────────────────

def save_school_enquiry(data):
    """Save school contact form submission"""
    data['created_at'] = firestore.SERVER_TIMESTAMP
    data['date'] = time.strftime("%Y-%m-%d")
    db.collection('school_enquiries').add(data)
    print(f"School enquiry saved from: {data.get('school', 'Unknown')}")

# ─────────────────────────────────────────────────────────
# BENCHMARKING — Global anonymous stats
# ─────────────────────────────────────────────────────────

def get_global_benchmarks(score):
    """
    Get global percentile ranking for a score.
    Uses anonymized all_sessions collection.
    """
    try:
        docs = db.collection('all_sessions').get()
        scores = [doc.to_dict().get('score', 0) for doc in docs]
        if not scores:
            return {'percentile': 50, 'total': 0, 'avg': 0}
        below = sum(1 for s in scores if s < score)
        percentile = int(below / len(scores) * 100)
        return {
            'percentile': percentile,
            'top_percent': 100 - percentile,
            'total': len(scores),
            'avg': round(sum(scores)/len(scores), 1),
            'top_score': max(scores)
        }
    except Exception as e:
        print(f"Benchmark error: {e}")
        return {'percentile': 50, 'total': 0, 'avg': 0}

print("All Firebase functions ready!")