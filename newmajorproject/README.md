# 🚀 Productivity Learning App

A beautiful, gamified productivity app that fetches real educational content from YouTube, NewsAPI, and RSS feeds, filtering out non-educational material to provide curated learning experiences.

## ✨ Features

- **🎓 Educational Content Only**: Automatically filters content to show only educational topics
- **📺 YouTube Integration**: Fetches educational videos from multiple categories
- **📰 News Articles**: Gets latest educational news from technology, science, health, and business
- **📰 RSS Feeds**: Aggregates content from BBC Science, ScienceDaily, NASA, and NYT Science
- **🤖 AI Summaries**: GPT-powered intelligent content summarization (optional)
- **🎮 Gamification**: Earn XP, level up, and track progress
- **⏱️ Focus Timer**: Built-in Pomodoro-style timer for focused learning sessions
- **🔍 Smart Search**: Search through all educational content
- **📱 Responsive Design**: Beautiful web interface that works in Chrome browser
- **⚡ Real-time Updates**: Fresh content fetched from APIs on each load
- **🔄 Live Content**: Click "Get Real-time Content" to fetch fresh videos and articles instantly

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Google YouTube Data API v3 key
- NewsAPI key

### 1. Install Dependencies
```bash
pip install flask requests google-api-python-client feedparser
```

### 2. Configure API Keys
Edit the following files with your API keys:

**backend/fetch/youtube.py**:
```python
API_KEY = "your_youtube_api_key_here"
```

**backend/fetch/news.py**:
```python
API_KEY = "your_newsapi_key_here"
```

### 3. Run the Application

#### Option A: One-Click Launcher (Windows)
```bash
start_app.bat
```

#### Option B: Manual Start
```bash
# Terminal 1: Start Backend API
python backend/app.py

# Terminal 2: Start Web Server
python web_server.py
```

#### Option C: Separate Batch Files
```bash
# Start Backend
start_backend.bat

# In another terminal/command prompt:
# Start Web Frontend
start_web.bat
```

### 4. Open in Browser
Navigate to: http://127.0.0.1:8000

## 📊 Content Categories

The app filters content into these educational categories:
- **Science & Technology**: Physics, chemistry, biology, computer science
- **Mathematics**: Algebra, calculus, statistics, data science
- **History & Social Studies**: World history, economics, politics
- **Language & Literature**: Writing, grammar, literature analysis
- **Health & Medicine**: Anatomy, nutrition, mental health
- **Business & Finance**: Entrepreneurship, marketing, economics
- **Arts & Design**: Digital art, graphic design, creative writing
- **Environment**: Climate science, sustainability, ecology

## 🎯 How to Use

1. **Browse Content**: View educational videos, articles, and blog posts
2. **Get Real-time Content**: Click "Get Real-time Content" or "Get Real-time Video" to fetch fresh content from APIs
3. **Search**: Use the search bar to find specific topics (searches through all content)
4. **Start Timer**: Click "Start Focus Session" for timed learning (5, 10, or 15 minutes)
5. **Stop Timer**: Click "Stop Session" button to end focus sessions early
6. **AI Summaries**: Click the "AI Summary" button on any content card for intelligent summaries
7. **Track Progress**: Earn XP by reading articles and watching videos
8. **Level Up**: Reach new levels as you learn more

## 🤖 AI Summary Feature

The app includes AI-powered content summarization using OpenAI GPT:

### Current Status: ✅ **ENABLED** (Basic Mode)
- **Basic Summaries**: Working now with smart text extraction
- **AI Summaries**: Ready to upgrade with OpenAI API key

### Setup AI Summaries (Optional Upgrade)
1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Run `setup_openai.bat` and enter your API key
3. Or set environment variable: `set OPENAI_API_KEY=your_actual_api_key_here`
4. Restart the backend server

### How It Works
- **With API Key**: Uses GPT-3.5-turbo for intelligent, contextual summaries (2-3 sentences)
- **Without API Key**: Provides smart text extraction summaries (currently active)
- **XP Rewards**: Earn 5 XP for each AI summary generated

### API Endpoint
```
GET /summarize/<item_id>
```
Returns JSON with summary, summary type (ai/basic), and metadata.

## 🔧 API Endpoints

- `GET /content` - Get all educational content
- `GET /content/<type>` - Filter by type (video, news, blog)
- `GET /content/category/<category>` - Filter by educational category
- `POST /search` - Search content with keyword matching
- `GET /progress` - Get user progress
- `POST /start_timer/<minutes>` - Start focus timer
- `GET /timer_status` - Check timer status
- `GET /summarize/<item_id>` - Get AI summary of content

## 🏗️ Project Structure

```
├── simple_backend.py          # Main Flask API server
├── web_server.py             # Web server for frontend
├── web_frontend.html          # Beautiful web interface
├── start_app.bat             # One-click launcher
├── backend/
│   ├── fetch/
│   │   ├── youtube.py        # YouTube API integration
│   │   ├── news.py          # NewsAPI integration
│   │   └── rss.py           # RSS feed parsing
│   └── app.py               # Legacy backend (not used)
├── utils/
│   └── filter.py            # Educational content filtering
└── README.md                # This file
```

## 🔍 Content Filtering

The app uses intelligent keyword-based filtering to ensure only educational content is displayed. It checks for:
- Educational keywords in titles and descriptions
- Academic subject areas
- Learning-focused content
- Excludes entertainment, sports, and non-educational topics

## 🎮 Gamification System

- **XP System**: Earn points for reading articles and watching videos
- **Levels**: Progress through levels as you accumulate XP
- **Achievements**: Unlock badges for different learning milestones
- **Progress Tracking**: Monitor your learning journey

## 🌐 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 🐛 Troubleshooting

### Backend won't start
- Check that all dependencies are installed: `pip install flask requests google-api-python-client feedparser`
- Verify API keys are correctly set in the fetch files
- Make sure ports 5000 and 8000 are not in use

### No content appears
- Check API keys are valid and have quota remaining
- Verify internet connection
- Check console for API error messages

### Web interface doesn't load
- Ensure both backend (port 5000) and web server (port 8000) are running
- Try refreshing the page
- Check browser console for JavaScript errors

## 📈 Performance

- Content is cached in memory for fast loading
- API calls are optimized to stay within rate limits
- Filtering happens server-side for better performance
- Responsive design works on all screen sizes

## 🔒 Security

- API keys are stored locally (never committed to version control)
- No user data is stored or transmitted
- All content is fetched from reputable educational sources

---

**Happy Learning! 🎓✨**
4. (Optional) Configure API keys in environment variables

## 🚀 Running the App

### **Option 1: Web Version (Recommended - Opens in Chrome)**

**Quick Start (Easiest):**
```bash
# Double-click this file to start both servers automatically
start_web_app.bat
```

**Or manually:**
```bash
# Terminal 1: Start Backend
python simple_backend.py

# Terminal 2: Start Web Server
python web_server.py
```

**Then open Chrome and go to:** `http://127.0.0.1:8000`

### **Option 2: Desktop App Version**

```bash
# Terminal 1: Start Backend
python simple_backend.py

# Terminal 2: Start Desktop App
python main.py
```

## 🎮 How to Use

### Getting Started
1. Launch the app using the commands above
2. Browse content in different tabs (Home, Shorts, Videos, Blogs)
3. Use semantic search to find specific topics
4. Start a timer session for focused learning

### Gamification
- Earn XP by completing content and sessions
- Level up to unlock new features and content
- Track progress on the gamification roadmap

### Focus Features
- Set timer sessions with automatic focus lock
- AI summarizes content for efficient learning
- Doomscrolling detection prevents unhealthy habits

## 📁 Project Structure

```
├── main.py                 # Enhanced Kivy frontend with all features
├── simple_backend.py       # Standalone backend with mock data
├── backend/
│   ├── app.py             # Full Flask API
│   ├── db.py              # Database utilities
│   └── fetch/
│       ├── news.py        # News API fetcher
│       ├── rss.py         # RSS feed fetcher
│       └── youtube.py     # YouTube API fetcher
├── utils/
│   └── filter.py          # BERT content classification
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Environment Variables
```bash
# API Keys (optional - mock data used if not provided)
YOUTUBE_API_KEY=your_key
NEWS_API_KEY=your_key
OPENAI_API_KEY=your_key

# Database (optional - in-memory used if not provided)
MONGODB_URI=mongodb://localhost:27017/productivity_app
```

### Mock Data
The app includes comprehensive mock data fallbacks for all external APIs, so it works completely offline.

## 🎯 Key Features Implemented

✅ **Tabbed Navigation**: Home grid, Shorts vertical scroll, Videos, Blogs
✅ **Content Cards**: Rich content display with thumbnails and metadata
✅ **Semantic Search**: GPT-powered intelligent search
✅ **Timer Sessions**: Focus sessions with automatic progression
✅ **Focus Lock**: Prevents distractions during sessions
✅ **Gamification**: XP system, leveling, achievement roadmap
✅ **AI Summarization**: Content summaries for efficient learning
✅ **Doomscrolling Detection**: Behavioral monitoring with break suggestions
✅ **Responsive UI**: Works on multiple screen sizes
✅ **Offline Mode**: Full functionality without external APIs

## 🐛 Troubleshooting

### Common Issues
- **Import Errors**: Ensure all dependencies are installed
- **API Failures**: App automatically falls back to mock data
- **UI Issues**: Check Kivy installation and graphics drivers
- **Performance**: Close other applications for better performance

### Debug Mode
Run with debug logging:
```bash
python main.py --debug
```

## 📈 Future Enhancements

- Mobile app versions (iOS/Android)
- Advanced analytics and learning insights
- Social features and study groups
- Integration with learning management systems
- Custom content creation tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for productive learning experiences**