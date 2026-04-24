from urllib.parse import urlparse

# A dictionary of well-known sources with their credibility ratings.
# Scores are out of 10.
# Bias labels indicate political lean or focus.
KNOWN_SOURCES = {
    'bbc': {'score': 9.2, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'bbc news': {'score': 9.2, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'reuters': {'score': 9.5, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'associated press': {'score': 9.5, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'ap': {'score': 9.5, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'the new york times': {'score': 8.8, 'label': 'Reliable', 'bias': 'Left-Center', 'verified': True},
    'new york times': {'score': 8.8, 'label': 'Reliable', 'bias': 'Left-Center', 'verified': True},
    'nytimes': {'score': 8.8, 'label': 'Reliable', 'bias': 'Left-Center', 'verified': True},
    'al jazeera': {'score': 8.0, 'label': 'Reliable', 'bias': 'Left-Center', 'verified': True},
    'aljazeera': {'score': 8.0, 'label': 'Reliable', 'bias': 'Left-Center', 'verified': True},
    'the guardian': {'score': 8.5, 'label': 'Reliable', 'bias': 'Left', 'verified': True},
    'techcrunch': {'score': 8.9, 'label': 'Reliable', 'bias': 'Tech', 'verified': True},
    'the verge': {'score': 8.5, 'label': 'Reliable', 'bias': 'Tech', 'verified': True},
    'ars technica': {'score': 9.0, 'label': 'Reliable', 'bias': 'Tech', 'verified': True},
    'science daily': {'score': 9.4, 'label': 'Reliable', 'bias': 'Science', 'verified': True},
    'sciencedaily': {'score': 9.4, 'label': 'Reliable', 'bias': 'Science', 'verified': True},
    'nasa': {'score': 9.8, 'label': 'Highly Reliable', 'bias': 'Science', 'verified': True},
    'webmd': {'score': 8.0, 'label': 'Reliable', 'bias': 'Health', 'verified': True},
    'espn': {'score': 8.5, 'label': 'Reliable', 'bias': 'Sports', 'verified': True},
    'cnn': {'score': 7.5, 'label': 'Mostly Reliable', 'bias': 'Left', 'verified': True},
    'fox news': {'score': 5.5, 'label': 'Mixed Reliability', 'bias': 'Right', 'verified': True},
    'bloomberg': {'score': 9.1, 'label': 'Reliable', 'bias': 'Center', 'verified': True},
    'wall street journal': {'score': 8.9, 'label': 'Reliable', 'bias': 'Right-Center', 'verified': True},
    'wsj': {'score': 8.9, 'label': 'Reliable', 'bias': 'Right-Center', 'verified': True},
}

def get_source_name(article):
    # Try multiple fields that might contain the source
    source = article.get('feed_source') or article.get('source_name') or article.get('source')
    
    if not source and article.get('url'):
        # Extract from URL domain
        try:
            domain = urlparse(article.get('url')).netloc
            # remove www.
            if domain.startswith('www.'):
                domain = domain[4:]
            # grab the main name
            parts = domain.split('.')
            if len(parts) >= 2:
                source = parts[-2]
            else:
                source = domain
        except:
            pass
            
    if not source:
        source = 'Unknown'
        
    return source

def get_indicator_circle(score):
    if score >= 8.5:
        return '🟢' # Green
    elif score >= 6.5:
        return '🟡' # Yellow
    else:
        return '🔴' # Red

def enrich_with_credibility(article):
    source_name = str(get_source_name(article)).lower().strip()
    
    # Try exact match
    rating = KNOWN_SOURCES.get(source_name)
    
    # Try partial match if no exact match
    if not rating:
        for known, data in KNOWN_SOURCES.items():
            if known in source_name or source_name in known:
                rating = data
                break
                
    if not rating:
        # Default for unknown sources
        rating = {'score': 5.0, 'label': 'Unknown Reliability', 'bias': 'Unknown', 'verified': False}
        
    article['credibility_score'] = rating['score']
    article['credibility_label'] = rating['label']
    article['bias'] = rating['bias']
    article['verified'] = rating['verified']
    article['credibility_indicator'] = get_indicator_circle(rating['score'])
    
    # Overwrite source with a clean Title Case string for display purposes, 
    # but don't overwrite if it's already nicely formatted and we didn't find a match
    display_source = article.get('feed_source') or article.get('source_name') or article.get('source') or get_source_name(article)
    article['display_source'] = display_source.title() if isinstance(display_source, str) else str(display_source)
    
    return article
