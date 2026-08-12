import json

def compute_burnout_label(session):
    """
    Reuse the same logic from scorer.py's predict_burnout()
    A session is labeled 'burnout' if score was low AND duration was short
    (proxy for: they quit because they were tired)
    """
    score = session.get('score', 50)
    duration = session.get('duration', 0)
    stress = session.get('emotions', {}).get('stress', 0)
    boreout = session.get('emotions', {}).get('boreout', 0)
    
    # This mirrors your scorer.py trend logic, applied retroactively
    burnout = 1 if (score < 45 and (stress > 50 or boreout > 50)) else 0
    return burnout

def label_all():
    with open('training_data_raw.json') as f:
        sessions = json.load(f)
    
    for s in sessions:
        s['label_burnout'] = compute_burnout_label(s)
    
    with open('training_data_labeled.json', 'w') as f:
        json.dump(sessions, f, indent=2)
    
    positives = sum(s['label_burnout'] for s in sessions)
    print(f"Labeled {len(sessions)} sessions — {positives} burnout, {len(sessions)-positives} not")

if __name__ == '__main__':
    label_all()