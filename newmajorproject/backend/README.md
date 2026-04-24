# Productivity Hub Backend

Flask REST API for content aggregation and focus timer management.

## Features

- **Multi-source Content Aggregation**: YouTube, NewsAPI, RSS feeds
- **Smart Content Filtering**: AI-powered relevance scoring
- **MongoDB Storage**: Persistent content storage
- **Focus Timer API**: Session management for productivity
- **RESTful Endpoints**: Clean API design

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys in the respective files:
   - `fetch/news.py`: NewsAPI key
   - `fetch/youtube.py`: YouTube Data API key
   - `db.py`: MongoDB Atlas connection string

3. Run the server:
```bash
python app.py
```

## API Endpoints

### Content Management
- `GET /` - Health check
- `GET /content` - Get all stored content
- `GET /content/<type>` - Get content by type (news/video/blog)
- `GET /latest` - Get latest 20 items
- `GET /fetch` - Trigger content fetching from all sources

### Timer Management
- `GET /start_timer/<minutes>` - Start timer session
- `GET /timer_status` - Get current timer status

## Content Sources

### YouTube API
- Searches for educational content
- Keywords: science, technology, education
- Returns video titles and descriptions

### NewsAPI
- Technology category headlines
- English language only
- Top headlines format

### RSS Feeds
- BBC Science & Environment
- XML parsing with feedparser
- Article summaries and titles

## Content Filtering

Uses keyword-based scoring system:
- Keywords: science, technology, education, research, ai, history
- Minimum score of 1 required for storage
- Case-insensitive matching

## Database Schema

Content document structure:
```json
{
  "title": "Article/Video Title",
  "description": "Content description",
  "type": "news|video|blog",
  "source": "newsapi|youtube|rss"
}
```

## Timer Sessions

Session management:
- Single user session support
- Start time and end time tracking
- Real-time remaining time calculation
- Status: running/ended/no active timer

## Error Handling

- API key validation
- Network request error handling
- Database connection management
- Graceful degradation on failures

## Security Notes

- API keys stored in code (consider environment variables for production)
- No authentication implemented
- Local development server only
- MongoDB Atlas connection string included