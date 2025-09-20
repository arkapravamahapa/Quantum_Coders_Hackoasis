from datetime import datetime, timedelta

def calculate_next_review(item):
    """
    Update an item's spaced-repetition schedule based on the user's performance grade.
    Returns the updated item with new scheduling data.
    """

    DEFAULT_EASE_FACTOR = 2.5
    EASY_INTERVAL_MULTIPLIER = 1.3
    GOOD_INTERVAL_MULTIPLIER = 1.2
    HARD_INTERVAL_MULTIPLIER = 1.1

    repetitions = item.get('repetitions', 0)
    interval = item.get('interval', 0)
    ease_factor = item.get('ease_factor', DEFAULT_EASE_FACTOR)

    item['last_reviewed'] = datetime.now().isoformat()

    if item['grade'] == 'Again':
        repetitions = 0
        interval = 1
        ease_factor = max(1.3, ease_factor - 0.2)

    elif item['grade'] == 'Hard':
        repetitions += 1
        interval *= HARD_INTERVAL_MULTIPLIER
        ease_factor = max(1.3, ease_factor - 0.15)

    elif item['grade'] == 'Good':
        repetitions += 1
        interval *= GOOD_INTERVAL_MULTIPLIER
        if repetitions == 1:
            interval = 6
        ease_factor += 0.1

    elif item['grade'] == 'Easy':
        repetitions += 1
        interval *= EASY_INTERVAL_MULTIPLIER
        if repetitions == 1:
            interval = 6
        ease_factor += 0.15

    if interval < 1 and item['grade'] != 'Again':
        interval = 1

    item['repetitions'] = repetitions
    item['interval'] = round(interval)
    item['ease_factor'] = ease_factor
    item['next_review'] = (datetime.now() + timedelta(days=interval)).isoformat()

    return item


def get_cards_due_today(user_progress):
    """
    Return a list of cards that are scheduled for review today (or earlier).
    """
    today = datetime.now().date()
    due_cards = []

    for card_id, card_data in user_progress.items():
        if 'next_review' in card_data:
            next_review_date = datetime.fromisoformat(card_data['next_review']).date()
            if next_review_date <= today:
                due_cards.append(card_data)

    return due_cards
