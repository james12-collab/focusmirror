import json
import random

def augment(sessions, multiplier=5):
    """Create realistic variations of real sessions"""
    augmented = list(sessions)  # keep originals
    
    for _ in range(multiplier):
        for s in sessions:
            new_s = dict(s)
            # Jitter numeric fields by small realistic amounts
            new_s['score'] = max(0, min(100, s['score'] + random.randint(-8, 8)))
            new_s['duration'] = max(0.5, s['duration'] + random.uniform(-1, 1))
            emotions = dict(s.get('emotions', {}))
            for k in emotions:
                emotions[k] = max(0, min(100, emotions[k] + random.randint(-10, 10)))
            new_s['emotions'] = emotions
            # Recompute label from jittered values so it stays consistent
            from generate_labels import compute_burnout_label
            new_s['label_burnout'] = compute_burnout_label(new_s)
            augmented.append(new_s)
    
    return augmented

if __name__ == '__main__':
    with open('training_data_labeled.json') as f:
        sessions = json.load(f)
    
    final = augment(sessions, multiplier=8)
    
    with open('training_data_final.json', 'w') as f:
        json.dump(final, f, indent=2)
    
    print(f"Final dataset: {len(final)} sessions ({len(sessions)} real + synthetic)")