import importlib.util

# Detect optional PyTorch availability without importing it at module import time
TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None
if TORCH_AVAILABLE:
    print("PyTorch available")
else:
    print("PyTorch not available - transformer models will be skipped")

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
    print("Transformers library available")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None
    print("Transformers library not available - using keyword fallback")

# Try to load the classifier only when both transformers and PyTorch are available
classifier = None
MODEL_LOADED = False

if TRANSFORMERS_AVAILABLE and TORCH_AVAILABLE and pipeline is not None:
    try:
        # Load zero-shot classifier for content classification
        print("Loading BERT model for content classification... (this may take a moment)")
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        MODEL_LOADED = True
        print("BERT model loaded successfully for content classification")
    except Exception as e:
        print(f"Warning: Could not load BERT model: {e}")
        MODEL_LOADED = False
        classifier = None
elif TRANSFORMERS_AVAILABLE and not TORCH_AVAILABLE:
    MODEL_LOADED = False
    classifier = None
    print("Transformers is installed, but PyTorch is unavailable; skipping model load")
else:
    MODEL_LOADED = False
    classifier = None
    print("Using keyword-based content classification (AI model not available)")

# Categories considered productive
PRODUCTIVE_CATEGORIES = ["science", "technology", "education", "research", "history", "news", "politics", "academic", "learning", "biology", "mathematics", "psychology", "environment", "physics", "chemistry", "engineering"]

def classify_content(text):
    """Use zero-shot classification to determine if content is productive"""
    if not MODEL_LOADED or classifier is None:
        # Fallback to keyword matching
        return any(keyword in text.lower() for keyword in ["science", "technology", "education", "research", "history", "news", "politics", "biology", "mathematics", "psychology", "environment", "physics", "chemistry", "engineering"])

    if not text:
        return False

    try:
        result = classifier(text[:512], PRODUCTIVE_CATEGORIES, multi_label=True)
        # Check if any productive category has high confidence
        max_score = max(result['scores'])
        return max_score > 0.5  # Threshold for usefulness
    except Exception as e:
        print(f"Classification error: {e}")
        return False

def is_useful(item):
    """Determine if content is useful"""
    title = item.get("title", "")
    description = item.get("description", "")
    text = title + " " + description

    return classify_content(text)