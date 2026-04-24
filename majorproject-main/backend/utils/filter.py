KEYWORDS = ["science", "technology", "education", "research", "ai", "history"]

def utility_score(text):
    if not text:
        return 0

    text = text.lower()
    score = 0

    for word in KEYWORDS:
        if word in text:
            score += 1

    return score


def is_useful(item):
    title = item.get("title", "")
    description = item.get("description", "")

    text = title + " " + description

    return utility_score(text) >= 1