"""
Content filtering utility for educational content
Uses keyword-based filtering (BERT optional)
"""

import importlib.util
import re

# Detect optional PyTorch availability without importing it at module import time
TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None
if TORCH_AVAILABLE:
    print("PyTorch available")
else:
    print("PyTorch not available - transformer models will be skipped")

try:
    from transformers import pipeline
    BERT_AVAILABLE = True
    print("Transformers library available")
except ImportError:
    BERT_AVAILABLE = False
    pipeline = None
    print("Transformers library not available - using keyword filtering only")

# Try to load the classifier only when both transformers and PyTorch are available
classifier = None
if BERT_AVAILABLE and TORCH_AVAILABLE and pipeline is not None:
    try:
        # Load zero-shot classifier for content categorization
        print("Loading BERT model for content classification... (this may take a moment)")
        classifier = pipeline("zero-shot-classification",
                             model="facebook/bart-large-mnli",
                             device=-1)
        print("BERT model loaded successfully for content classification")
    except Exception as e:
        print(f"Warning: Could not load BERT model: {e}")
        BERT_AVAILABLE = False
        classifier = None
elif BERT_AVAILABLE and not TORCH_AVAILABLE:
    classifier = None
    print("Transformers is installed, but PyTorch is unavailable; skipping model load")
else:
    BERT_AVAILABLE = False
    classifier = None
    print("Using keyword-based content classification (AI model not available)")

# Educational keywords and categories
EDUCATIONAL_KEYWORDS = {
    'science': ['science', 'physics', 'chemistry', 'biology', 'astronomy', 'geology', 'mathematics', 'math',
                'quantum', 'theory', 'research', 'study', 'experiment', 'discovery', 'breakthrough'],
    'technology': ['technology', 'computer', 'programming', 'coding', 'software', 'hardware', 'ai', 'artificial intelligence',
                   'machine learning', 'data science', 'algorithm', 'blockchain', 'cybersecurity', 'robotics'],
    'education': ['education', 'learning', 'teaching', 'tutorial', 'course', 'lesson', 'guide', 'how to', 'explained',
                  'understanding', 'basics', 'fundamentals', 'introduction', 'beginner'],
    'health': ['health', 'medical', 'medicine', 'disease', 'treatment', 'therapy', 'clinical', 'pharmaceutical',
               'vaccination', 'epidemiology', 'physiology', 'anatomy', 'neuroscience'],
    'environment': ['environment', 'climate', 'sustainability', 'ecology', 'conservation', 'renewable', 'green energy',
                    'pollution', 'biodiversity', 'wildlife', 'ocean', 'forest', 'carbon'],
    'history': ['history', 'historical', 'civilization', 'archaeology', 'ancient', 'medieval', 'renaissance',
                'industrial revolution', 'world war', 'colonial', 'empire'],
    'economics': ['economics', 'finance', 'market', 'investment', 'banking', 'trade', 'policy', 'growth',
                  'inflation', 'unemployment', 'gdp', 'stock market', 'cryptocurrency'],
    'psychology': ['psychology', 'mental health', 'behavior', 'cognitive', 'neuroscience', 'therapy', 'disorder',
                   'personality', 'development', 'social psychology', 'clinical psychology']
}

# Categories that are considered productive or educational
PRODUCTIVE_CATEGORIES = [
    'science', 'technology', 'education', 'research', 'history', 'news', 'politics', 'academic', 'learning',
    'biology', 'mathematics', 'psychology', 'environment', 'physics', 'chemistry', 'engineering'
]

# Non-educational content to filter out
NON_EDUCATIONAL_KEYWORDS = [
    'celebrity', 'gossip', 'entertainment', 'sports', 'music', 'movie', 'film', 'tv show', 'celebrity news',
    'fashion', 'beauty', 'lifestyle', 'travel', 'food', 'recipe', 'restaurant', 'shopping', 'gaming',
    'social media', 'viral', 'meme', 'funny', 'joke', 'comedy', 'humor', 'prank', 'challenge',
    'reality tv', 'award show', 'red carpet', 'hollywood', 'bollywood', 'k-pop', 'pop culture'
]

def is_useful(item):
    """
    Determine if content is educational and useful for learning
    """
    title = item.get('title', '').lower()
    description = item.get('description', '').lower()
    content_type = item.get('type', '')

    # Combine title and description for analysis
    full_text = f"{title} {description}"

    # Check for non-educational content first
    if contains_non_educational_keywords(full_text):
        return False

    # Check for educational keywords
    if contains_educational_keywords(full_text):
        return True

    # Use BERT classification if available
    if BERT_AVAILABLE:
        return bert_classify_educational(full_text)

    # Fallback: check for academic/scientific indicators
    return has_academic_indicators(full_text)

def contains_educational_keywords(text):
    """
    Check if text contains educational keywords
    """
    for category, keywords in EDUCATIONAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return True
    return False

def contains_non_educational_keywords(text):
    """
    Check if text contains non-educational keywords
    """
    for keyword in NON_EDUCATIONAL_KEYWORDS:
        if keyword in text:
            return True
    return False

def bert_classify_educational(text):
    """
    Use BERT to classify if content is educational
    """
    try:
        candidate_labels = ["educational", "entertainment", "news", "sports", "lifestyle"]
        result = classifier(text[:512], candidate_labels)  # Limit text length

        # Check if educational is the top prediction or high confidence
        top_label = result['labels'][0]
        top_score = result['scores'][0]

        return top_label == "educational" and top_score > 0.3
    except Exception as e:
        print(f"BERT classification error: {e}")
        return False

def has_academic_indicators(text):
    """
    Check for academic/scientific indicators in text
    """
    indicators = [
        r'\b(dr\.|prof\.|ph\.d\.|research|study|university|college|academy)\b',
        r'\b(theory|hypothesis|experiment|methodology|analysis)\b',
        r'\b(data|statistics|evidence|findings|results)\b',
        r'\b(quantum|physics|chemistry|biology|mathematics)\b',
        r'\b(technology|computer|programming|algorithm)\b',
        r'\b(learn|teach|education|tutorial|course)\b'
    ]

    for pattern in indicators:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False

def get_content_category(text):
    """
    Determine the educational category of content
    """
    text_lower = text.lower()

    for category, keywords in EDUCATIONAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category

    return "general"

def filter_content_batch(items, min_confidence=0.6):
    """
    Filter a batch of content items and return only educational ones
    """
    filtered_items = []

    for item in items:
        if is_useful(item):
            # Add category information
            item['category'] = get_content_category(f"{item.get('title', '')} {item.get('description', '')}")
            filtered_items.append(item)

    return filtered_items

# Test function
if __name__ == "__main__":
    test_items = [
        {
            "title": "Introduction to Machine Learning",
            "description": "Learn the basics of ML algorithms and applications",
            "type": "video"
        },
        {
            "title": "Celebrity Gossip: Latest Hollywood News",
            "description": "Who wore what on the red carpet",
            "type": "news"
        },
        {
            "title": "Quantum Physics Explained",
            "description": "Understanding quantum mechanics and its applications",
            "type": "video"
        }
    ]

    print("Testing content filtering:")
    for item in test_items:
        is_educational = is_useful(item)
        category = get_content_category(f"{item['title']} {item['description']}")
        print(f"✓ {item['title'][:50]}... -> Educational: {is_educational}, Category: {category}")