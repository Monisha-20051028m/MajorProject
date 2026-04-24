import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock
import time

CONTENT_URL = "http://127.0.0.1:5000/content"
SEARCH_URL = "http://127.0.0.1:5000/search"
TIMER_START_URL = "http://127.0.0.1:5000/start_timer/"
TIMER_STATUS_URL = "http://127.0.0.1:5000/timer_status"
PROGRESS_URL = "http://127.0.0.1:5000/progress"
READ_URL = "http://127.0.0.1:5000/read/"
SUMMARIZE_URL = "http://127.0.0.1:5000/summarize/"


class ContentApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_start_time = time.time()
        self.doomscroll_warnings = 0
        self.current_category = "All"
        self.focus_locked = False
        self.timer_active = False
        self.timer_end_time = 0
        self.user_xp = 0
        self.user_level = 1
        self.scroll_events = []
        self.doomscroll_warnings = 0
        self.current_category = 'All'

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # 🔹 Top Navigation Bar with Categories
        self.top_nav = BoxLayout(size_hint=(1, 0.08), spacing=5, padding=5)
        categories = ['All', 'Science', 'Technology', 'History', 'News', 'Education', 'Research']
        for cat in categories:
            btn = Button(text=cat, size_hint=(None, 1), width=dp(80), font_size=12)
            btn.bind(on_press=lambda x, c=cat: self.filter_by_category(c))
            self.top_nav.add_widget(btn)
        self.root.add_widget(self.top_nav)

        # 🔹 Status Bar (Timer, Progress, Focus Lock)
        status_bar = BoxLayout(size_hint=(1, 0.08))

        # Timer section
        timer_section = BoxLayout(orientation='vertical', size_hint=(0.25, 1))
        self.timer_label = Label(text="No Timer", font_size=14)
        timer_section.add_widget(self.timer_label)

        timer_btns = BoxLayout(size_hint=(1, 0.6))
        for mins in [5, 10, 15]:
            btn = Button(text=f"{mins}min", font_size=12)
            btn.bind(on_press=lambda x, m=mins: self.start_timer(m))
            timer_btns.add_widget(btn)
        timer_section.add_widget(timer_btns)
        status_bar.add_widget(timer_section)

        # Progress section
        progress_section = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        self.progress_label = Label(text="Level 1 - 0 XP", font_size=12)
        progress_section.add_widget(self.progress_label)

        self.xp_progress = ProgressBar(max=100, value=0, size_hint=(1, 0.4))
        progress_section.add_widget(self.xp_progress)
        status_bar.add_widget(progress_section)

        # Search and Controls section
        control_section = BoxLayout(orientation='vertical', size_hint=(0.45, 1))
        search_row = BoxLayout(size_hint=(1, 0.5))
        self.search_input = TextInput(hint_text="Search topics...", multiline=False)
        search_row.add_widget(self.search_input)

        search_btn = Button(text="🔍", size_hint=(None, 1), width=dp(50))
        search_btn.bind(on_press=self.perform_search)
        search_row.add_widget(search_btn)
        control_section.add_widget(search_row)

        control_row = BoxLayout(size_hint=(1, 0.5))
        self.focus_lock_btn = Button(text="🔓 Unlock", font_size=12)
        self.focus_lock_btn.bind(on_press=self.toggle_focus_lock)
        control_row.add_widget(self.focus_lock_btn)

        roadmap_btn = Button(text="🗺️ Roadmap", font_size=12)
        roadmap_btn.bind(on_press=self.show_roadmap)
        control_row.add_widget(roadmap_btn)
        control_section.add_widget(control_row)
        status_bar.add_widget(control_section)

        self.root.add_widget(status_bar)

        # 🔹 Timer Buttons
        timer_bar = BoxLayout(size_hint=(1, 0.08))
        timer_bar.add_widget(Button(text="5 Min", on_press=lambda x: self.start_timer(5)))
        timer_bar.add_widget(Button(text="10 Min", on_press=lambda x: self.start_timer(10)))
        timer_bar.add_widget(Button(text="15 Min", on_press=lambda x: self.start_timer(15)))
        self.root.add_widget(timer_bar)

        # 🔹 Progress Bar
        progress_bar_container = BoxLayout(size_hint=(1, 0.05))
        self.xp_progress = ProgressBar(max=100, value=0, size_hint=(0.8, 1))
        progress_bar_container.add_widget(self.xp_progress)
        progress_bar_container.add_widget(Label(text="", size_hint=(0.2, 1)))  # Spacer
        self.root.add_widget(progress_bar_container)

        # 🔹 Main Content Area with Tabs
        self.tabs = TabbedPanel(do_default_tab=False, size_hint=(1, 0.76))

        # Home Tab - Grid layout like YouTube
        home_tab = TabbedPanelItem(text='🏠 Home')
        self.home_scroll = ScrollView()
        self.home_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        self.home_grid.bind(minimum_height=self.home_grid.setter('height'))
        self.home_scroll.add_widget(self.home_grid)
        home_tab.add_widget(self.home_scroll)
        self.tabs.add_widget(home_tab)

        # Shorts Tab - Vertical scrolling like YouTube Shorts
        shorts_tab = TabbedPanelItem(text='⚡ Shorts')
        self.shorts_scroll = ScrollView()
        self.shorts_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=5)
        self.shorts_layout.bind(minimum_height=self.shorts_layout.setter('height'))
        self.shorts_scroll.add_widget(self.shorts_layout)
        shorts_tab.add_widget(self.shorts_scroll)
        self.tabs.add_widget(shorts_tab)

        # Videos Tab
        videos_tab = TabbedPanelItem(text='🎥 Videos')
        self.videos_scroll = ScrollView()
        self.videos_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=5)
        self.videos_layout.bind(minimum_height=self.videos_layout.setter('height'))
        self.videos_scroll.add_widget(self.videos_layout)
        videos_tab.add_widget(self.videos_scroll)
        self.tabs.add_widget(videos_tab)

        # Blogs Tab
        blogs_tab = TabbedPanelItem(text='📖 Blogs')
        self.blogs_scroll = ScrollView()
        self.blogs_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5, padding=5)
        self.blogs_layout.bind(minimum_height=self.blogs_layout.setter('height'))
        self.blogs_scroll.add_widget(self.blogs_layout)
        blogs_tab.add_widget(self.blogs_scroll)
        self.tabs.add_widget(blogs_tab)

        self.root.add_widget(self.tabs)

        # 🔹 Initialize
        self.load_content()
        # self.load_progress()  # Commented out - method doesn't exist yet

        # 🔹 Timer and monitoring loops
        Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.monitor_doomscrolling, 5)  # Check every 5 seconds

        return self.root

    # 📥 Load content
    def load_content(self):
        try:
            response = requests.get(CONTENT_URL, timeout=5)
            data = response.json()

            # Clear existing content
            self.home_grid.clear_widgets()
            self.shorts_layout.clear_widgets()
            self.videos_layout.clear_widgets()
            self.blogs_layout.clear_widgets()

            for item in data:
                title = item.get("title", "No Title")
                content_type = item.get("type", "unknown")
                description = item.get("description", "")[:100] + "..." if len(item.get("description", "")) > 100 else item.get("description", "")

                # Create content card
                card = self.create_content_card(item, title, description)

                # Add to appropriate tabs
                if content_type == "video":
                    # Add to home grid and videos tab
                    self.home_grid.add_widget(card)
                    self.videos_layout.add_widget(self.create_content_card(item, title, description))

                    # Add short version to shorts tab (first 3 videos)
                    if len(self.shorts_layout.children) < 6:
                        short_card = self.create_short_card(item, title)
                        self.shorts_layout.add_widget(short_card)

                elif content_type in ["news", "blog"]:
                    # Add to home grid and blogs tab
                    self.home_grid.add_widget(card)
                    self.blogs_layout.add_widget(self.create_content_card(item, title, description))

        except requests.exceptions.ConnectionError:
            # Backend not running - show helpful message
            error_msg = "Backend not running. Please start the backend first:\npython simple_backend.py"
            error_label = Label(text=error_msg, size_hint_y=None, height=60, halign='center')
            self.home_grid.add_widget(error_label)
        except Exception as e:
            # Other errors - show generic message
            error_msg = f"Error loading content: {str(e)}"
            error_label = Label(text=error_msg, size_hint_y=None, height=40)
            self.home_grid.add_widget(error_label)

    def create_content_card(self, item, title, description):
        """Create a content card for grid layout"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=5, spacing=5)
        card.canvas.before.add(Color(0.9, 0.9, 0.9, 1))
        card.canvas.before.add(Rectangle(size=card.size, pos=card.pos))

        title_label = Label(text=title[:30] + "..." if len(title) > 30 else title,
                           font_size=14, bold=True, size_hint_y=None, height=dp(30))
        card.add_widget(title_label)

        desc_label = Label(text=description, font_size=12, size_hint_y=None, height=dp(50))
        card.add_widget(desc_label)

        # Action buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(30), spacing=5)
        read_btn = Button(text="Read", font_size=12, size_hint=(0.5, 1))
        read_btn.bind(on_press=lambda x: self.open_content(item))
        btn_layout.add_widget(read_btn)

        summarize_btn = Button(text="📝", font_size=12, size_hint=(0.25, 1))
        summarize_btn.bind(on_press=lambda x: self.show_summary(item))
        btn_layout.add_widget(summarize_btn)

        card.add_widget(btn_layout)
        return card

    def create_short_card(self, item, title):
        """Create a short-form content card"""
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200), padding=10, spacing=5)
        card.canvas.before.add(Color(0.95, 0.95, 0.95, 1))
        card.canvas.before.add(Rectangle(size=card.size, pos=card.pos))

        title_label = Label(text=title[:40] + "..." if len(title) > 40 else title,
                           font_size=16, bold=True, size_hint_y=None, height=dp(40))
        card.add_widget(title_label)

        watch_btn = Button(text="▶️ Watch", size_hint_y=None, height=dp(40), font_size=14)
        watch_btn.bind(on_press=lambda x: self.open_content(item))
        card.add_widget(watch_btn)

        return card

    def filter_by_category(self, category):
        """Filter content by category"""
        self.current_category = category
        # Update category button colors
        for child in self.top_nav.children:
            if hasattr(child, 'text'):
                if child.text == category:
                    child.background_color = (0.3, 0.6, 1, 1)  # Blue for selected
                else:
                    child.background_color = (1, 1, 1, 1)  # White for others

        # Reload content with filter
        self.load_content()

    def show_roadmap(self, instance):
        """Show gamification roadmap"""
        roadmap_popup = Popup(title="🎯 Learning Roadmap", size_hint=(0.8, 0.8))

        roadmap_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Current progress
        progress_layout = BoxLayout(size_hint_y=None, height=dp(50))
        level_label = Label(text=f"Current Level: {self.progress_label.text.split()[1]}",
                           font_size=18, bold=True)
        progress_layout.add_widget(level_label)
        roadmap_layout.add_widget(progress_layout)

        # Roadmap milestones
        milestones = [
            "📚 Read 5 articles (10 XP each)",
            "🎥 Watch 3 videos (15 XP each)",
            "🏆 Complete first topic (50 XP bonus)",
            "⭐ Reach Level 5 (500 total XP)",
            "👑 Master 10 topics (1000 XP)",
            "🎓 Become a Learning Champion (2000 XP)"
        ]

        for milestone in milestones:
            milestone_label = Label(text=milestone, size_hint_y=None, height=dp(40),
                                   font_size=14, halign='left')
            roadmap_layout.add_widget(milestone_label)

        close_btn = Button(text="Close", size_hint_y=None, height=dp(50))
        close_btn.bind(on_press=roadmap_popup.dismiss)
        roadmap_layout.add_widget(close_btn)

        roadmap_popup.content = roadmap_layout
        roadmap_popup.open()

    def show_summary(self, item):
        """Show AI-generated summary of content"""
        try:
            # Find item index
            response = requests.get(CONTENT_URL, timeout=5)
            data = response.json()
            item_index = next((i for i, d in enumerate(data) if d.get("title") == item.get("title")), -1)

            if item_index >= 0:
                summary_response = requests.get(SUMMARIZE_URL + str(item_index), timeout=10)
                summary_data = summary_response.json()

                summary_popup = Popup(title="📝 Content Summary", size_hint=(0.9, 0.7))
                summary_layout = BoxLayout(orientation='vertical', padding=20)

                summary_text = summary_data.get('summary', 'Summary not available')
                summary_label = Label(text=summary_text, font_size=14, halign='left')
                summary_layout.add_widget(summary_label)

                close_btn = Button(text="Close", size_hint_y=None, height=dp(50))
                close_btn.bind(on_press=summary_popup.dismiss)
                summary_layout.add_widget(close_btn)

                summary_popup.content = summary_layout
                summary_popup.open()

        except Exception as e:
            error_popup = Popup(title="Error", size_hint=(0.6, 0.4))
            error_layout = BoxLayout(orientation='vertical', padding=20)
            error_layout.add_widget(Label(text=f"Could not generate summary: {str(e)}"))
            close_btn = Button(text="OK", size_hint_y=None, height=dp(40))
            close_btn.bind(on_press=error_popup.dismiss)
            error_layout.add_widget(close_btn)
            error_popup.content = error_layout
            error_popup.open()

    def monitor_doomscrolling(self, dt):
        """Monitor scrolling behavior for doomscrolling patterns"""
        current_time = time.time()

        # Track scroll events (simplified - in real app would track actual scroll)
        self.scroll_events.append(current_time)

        # Keep only last 10 minutes of events
        self.scroll_events = [t for t in self.scroll_events if current_time - t < 600]

        # Check for doomscrolling patterns
        if len(self.scroll_events) >= 10:  # At least 10 scroll events
            time_span = current_time - self.scroll_events[0]
            scroll_rate = len(self.scroll_events) / time_span

            # High scroll rate indicates potential doomscrolling
            if scroll_rate > 0.5:  # More than 0.5 scrolls per second
                self.doomscroll_warnings += 1
                if self.doomscroll_warnings >= 3:
                    self.show_doomscroll_warning()

    def show_doomscroll_warning(self):
        """Show warning about doomscrolling behavior"""
        warning_popup = Popup(title="⏰ Take a Break!", size_hint=(0.7, 0.5))
        warning_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        warning_layout.add_widget(Label(text="You've been scrolling quite a bit!", font_size=16))
        warning_layout.add_widget(Label(text="Consider taking a short break or switching topics.",
                                      font_size=14))

        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)
        continue_btn = Button(text="Continue", size_hint=(0.5, 1))
        continue_btn.bind(on_press=warning_popup.dismiss)
        btn_layout.add_widget(continue_btn)

        break_btn = Button(text="Take Break", size_hint=(0.5, 1))
        break_btn.bind(on_press=lambda x: self.take_break(warning_popup))
        btn_layout.add_widget(break_btn)

        warning_layout.add_widget(btn_layout)

        warning_popup.content = warning_layout
        warning_popup.open()

    def take_break(self, popup):
        """Handle break request"""
        popup.dismiss()
        self.doomscroll_warnings = 0  # Reset warnings

        break_popup = Popup(title="😌 Break Time", size_hint=(0.6, 0.4))
        break_layout = BoxLayout(orientation='vertical', padding=20)

        break_layout.add_widget(Label(text="Great! Take 5 minutes to relax."))
        break_layout.add_widget(Label(text="We'll remind you when your break is over."))

        ok_btn = Button(text="OK", size_hint_y=None, height=dp(40))
        ok_btn.bind(on_press=break_popup.dismiss)
        break_layout.add_widget(ok_btn)

        break_popup.content = break_layout
        break_popup.open()

    # 🔍 Perform semantic search
    def perform_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            return

        try:
            response = requests.post(SEARCH_URL, json={"query": query}, timeout=5)
            result = response.json()

            # Clear home tab and show search results
            self.home_grid.clear_widgets()

            topic_label = Label(text=f"🔍 Results for: {result.get('topic', query)}",
                               size_hint_y=None, height=dp(40), font_size=16, bold=True)
            self.home_grid.add_widget(topic_label)

            for item in result.get('results', []):
                title = item.get("title", "No Title")
                description = item.get("description", "")[:80] + "..." if len(item.get("description", "")) > 80 else item.get("description", "")
                card = self.create_content_card(item, title, description)
                self.home_grid.add_widget(card)

        except Exception as e:
            error_label = Label(text=f"Search Error: {str(e)}", size_hint_y=None, height=dp(40))
            self.home_grid.clear_widgets()
            self.home_grid.add_widget(error_label)

    # � Load user progress
    def load_progress(self):
        try:
            response = requests.get(PROGRESS_URL, timeout=5)
            progress = response.json()

            level = progress.get("level", 1)
            xp = progress.get("xp", 0)
            xp_needed = level * 100
            xp_progress = xp % 100

            self.progress_label.text = f"Level {level} - {xp}/{xp_needed} XP"
            self.xp_progress.value = xp_progress

        except Exception as e:
            print(f"Progress load error: {e}")

    # 📖 Open content and mark as read
    def open_content(self, item):
        # Mark as read and update progress
        try:
            # Find item index
            response = requests.get(CONTENT_URL, timeout=5)
            data = response.json()
            item_index = next((i for i, d in enumerate(data) if d.get("title") == item.get("title")), -1)

            if item_index >= 0:
                requests.post(READ_URL + str(item_index), timeout=5)
                self.load_progress()  # Refresh progress

                # Show content popup
                self.show_content_detail(item)

        except Exception as e:
            print(f"Error marking as read: {e}")

    def show_content_detail(self, item):
        """Show detailed content view"""
        content_popup = Popup(title=item.get("title", "Content"), size_hint=(0.9, 0.8))

        content_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Content details
        scroll = ScrollView()
        content_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        content_box.bind(minimum_height=content_box.setter('height'))

        title_label = Label(text=item.get("title", ""), font_size=18, bold=True,
                           size_hint_y=None, height=dp(50), halign='left')
        content_box.add_widget(title_label)

        desc_label = Label(text=item.get("description", ""),
                          font_size=14, size_hint_y=None, height=dp(100), halign='left')
        content_box.add_widget(desc_label)

        # Action buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)
        summarize_btn = Button(text="📝 Summarize", size_hint=(0.3, 1))
        summarize_btn.bind(on_press=lambda x: self.show_summary(item))
        btn_layout.add_widget(summarize_btn)

        close_btn = Button(text="Close", size_hint=(0.3, 1))
        close_btn.bind(on_press=content_popup.dismiss)
        btn_layout.add_widget(close_btn)

        content_box.add_widget(btn_layout)
        scroll.add_widget(content_box)
        content_layout.add_widget(scroll)

        content_popup.content = content_layout
        content_popup.open()

    # 🔒 Toggle focus lock
    def toggle_focus_lock(self, instance):
        if "🔒" in self.focus_lock_btn.text:
            self.focus_lock_btn.text = "🔓 Unlock"
            # Enable scrolling for all tabs
            self.home_scroll.do_scroll_y = True
            self.shorts_scroll.do_scroll_y = True
            self.videos_scroll.do_scroll_y = True
            self.blogs_scroll.do_scroll_y = True
        else:
            self.focus_lock_btn.text = "🔒 Lock"
            # Disable scrolling for all tabs
            self.home_scroll.do_scroll_y = False
            self.shorts_scroll.do_scroll_y = False
            self.videos_scroll.do_scroll_y = False
            self.blogs_scroll.do_scroll_y = False

    # ⏱️ Start timer
    def start_timer(self, minutes):
        try:
            requests.get(TIMER_START_URL + str(minutes), timeout=5)
            self.focus_lock_btn.text = "🔒 Lock"  # Auto-lock when timer starts
            self.toggle_focus_lock(None)  # Apply lock
        except:
            self.timer_label.text = "Backend Error"

    # ⏳ Update timer
    def update_timer(self, dt):
        try:
            res = requests.get(TIMER_STATUS_URL, timeout=5).json()

            if res["status"] == "running":
                self.timer_label.text = f"⏱️ {res['remaining']}s left"

            elif res["status"] == "ended":
                self.timer_label.text = "✅ Timer Ended"
                self.focus_lock_btn.text = "🔓 Unlock"
                self.toggle_focus_lock(None)  # Auto-unlock

                # Show completion popup
                self.show_timer_complete()

            else:
                self.timer_label.text = "No Active Timer"

        except:
            self.timer_label.text = "Backend Offline"

    def show_timer_complete(self):
        """Show timer completion popup"""
        complete_popup = Popup(title="🎉 Session Complete!", size_hint=(0.7, 0.5))
        complete_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        complete_layout.add_widget(Label(text="Great job completing your study session!", font_size=16))
        complete_layout.add_widget(Label(text="You've earned XP and made progress!", font_size=14))

        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=10)
        continue_btn = Button(text="Continue Learning", size_hint=(0.5, 1))
        continue_btn.bind(on_press=complete_popup.dismiss)
        btn_layout.add_widget(continue_btn)

        break_btn = Button(text="Take Break", size_hint=(0.5, 1))
        break_btn.bind(on_press=lambda x: self.take_break(complete_popup))
        btn_layout.add_widget(break_btn)

        complete_layout.add_widget(btn_layout)

        complete_popup.content = complete_layout
        complete_popup.open()


if __name__ == "__main__":
    ContentApp().run()