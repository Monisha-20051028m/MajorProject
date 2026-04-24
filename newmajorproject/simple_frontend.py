#!/usr/bin/env python3
"""
Simplified Productivity App Frontend
"""

import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock

# Backend URLs
CONTENT_URL = "http://127.0.0.1:5000/content"
SEARCH_URL = "http://127.0.0.1:5000/search"
TIMER_START_URL = "http://127.0.0.1:5000/start_timer/"
TIMER_STATUS_URL = "http://127.0.0.1:5000/timer_status"
PROGRESS_URL = "http://127.0.0.1:5000/progress"
READ_URL = "http://127.0.0.1:5000/read/"

class ContentApp(App):

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # Top Bar
        top_bar = BoxLayout(size_hint=(1, 0.1))

        # Timer section
        self.timer_label = Label(
            text="No Timer",
            size_hint=(0.3, 1),
            font_size=16
        )
        top_bar.add_widget(self.timer_label)

        # Search section
        self.search_input = TextInput(
            hint_text="Search topics...",
            size_hint=(0.4, 1),
            multiline=False
        )
        top_bar.add_widget(self.search_input)

        # Search button
        search_btn = Button(
            text="Search",
            size_hint=(0.15, 1),
            on_press=self.perform_search
        )
        top_bar.add_widget(search_btn)

        # Focus lock button
        self.focus_lock_btn = Button(
            text="🔓 Unlock",
            size_hint=(0.15, 1),
            on_press=self.toggle_focus_lock
        )
        top_bar.add_widget(self.focus_lock_btn)

        self.root.add_widget(top_bar)

        # Timer buttons
        timer_bar = BoxLayout(size_hint=(1, 0.08))
        timer_bar.add_widget(Button(text="5 Min", on_press=lambda x: self.start_timer(5)))
        timer_bar.add_widget(Button(text="10 Min", on_press=lambda x: self.start_timer(10)))
        timer_bar.add_widget(Button(text="15 Min", on_press=lambda x: self.start_timer(15)))
        self.root.add_widget(timer_bar)

        # Progress bar (simplified)
        self.progress_label = Label(
            text="Level 1 - 0 XP",
            size_hint=(1, 0.05),
            font_size=14
        )
        self.root.add_widget(self.progress_label)

        # Tabbed Content
        self.tabs = TabbedPanel(do_default_tab=False, size_hint=(1, 0.77))

        # Home Tab
        home_tab = TabbedPanelItem(text='Home')
        self.home_scroll = ScrollView()
        self.home_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.home_layout.bind(minimum_height=self.home_layout.setter('height'))
        self.home_scroll.add_widget(self.home_layout)
        home_tab.add_widget(self.home_scroll)
        self.tabs.add_widget(home_tab)

        # Videos Tab
        video_tab = TabbedPanelItem(text='Videos')
        self.video_scroll = ScrollView()
        self.video_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.video_layout.bind(minimum_height=self.video_layout.setter('height'))
        self.video_scroll.add_widget(self.video_layout)
        video_tab.add_widget(self.video_scroll)
        self.tabs.add_widget(video_tab)

        # Blogs Tab
        blog_tab = TabbedPanelItem(text='Blogs')
        self.blog_scroll = ScrollView()
        self.blog_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.blog_layout.bind(minimum_height=self.blog_layout.setter('height'))
        self.blog_scroll.add_widget(self.blog_layout)
        blog_tab.add_widget(self.blog_scroll)
        self.tabs.add_widget(blog_tab)

        self.root.add_widget(self.tabs)

        # Load initial content
        self.load_content()
        self.load_progress()

        # Timer update loop
        Clock.schedule_interval(self.update_timer, 1)

        return self.root

    def load_content(self):
        try:
            response = requests.get(CONTENT_URL, timeout=5)
            data = response.json()

            # Clear existing content
            self.home_layout.clear_widgets()
            self.video_layout.clear_widgets()
            self.blog_layout.clear_widgets()

            for i, item in enumerate(data):
                title = item.get("title", "No Title")
                content_type = item.get("type", "unknown")

                # Create content button
                btn = Button(
                    text=title[:50] + "..." if len(title) > 50 else title,
                    size_hint_y=None,
                    height=60,
                    halign='left',
                    valign='middle'
                )
                btn.bind(on_press=lambda x, idx=i: self.open_content(idx))

                # Add to appropriate tab
                if content_type == "video":
                    self.video_layout.add_widget(btn)
                elif content_type == "blog":
                    self.blog_layout.add_widget(btn)
                else:
                    self.home_layout.add_widget(btn)

        except Exception as e:
            # Show error message
            error_msg = f"Backend not running. Error: {str(e)}"
            self.home_layout.clear_widgets()
            self.home_layout.add_widget(Label(text=error_msg))

    def load_progress(self):
        try:
            response = requests.get(PROGRESS_URL, timeout=5)
            progress = response.json()

            level = progress.get("level", 1)
            xp = progress.get("xp", 0)
            xp_needed = level * 100

            self.progress_label.text = f"Level {level} - {xp}/{xp_needed} XP"

        except Exception as e:
            print(f"Progress load error: {e}")

    def perform_search(self, instance):
        query = self.search_input.text.strip()
        if not query:
            return

        try:
            response = requests.post(SEARCH_URL, json={"query": query}, timeout=5)
            result = response.json()

            # Clear home tab and show search results
            self.home_layout.clear_widgets()

            topic_label = Label(text=f"Results for: {result.get('topic', query)}", size_hint_y=None, height=40)
            self.home_layout.add_widget(topic_label)

            for i, item in enumerate(result.get('results', [])):
                title = item.get("title", "No Title")
                btn = Button(
                    text=title[:50] + "..." if len(title) > 50 else title,
                    size_hint_y=None,
                    height=60,
                    halign='left'
                )
                btn.bind(on_press=lambda x, idx=i: self.open_content(idx))
                self.home_layout.add_widget(btn)

        except Exception as e:
            error_label = Label(text=f"Search Error: {str(e)}", size_hint_y=None, height=40)
            self.home_layout.clear_widgets()
            self.home_layout.add_widget(error_label)

    def open_content(self, item_index):
        # Mark as read and update progress
        try:
            requests.post(READ_URL + str(item_index), timeout=5)
            self.load_progress()  # Refresh progress
        except Exception as e:
            print(f"Error marking as read: {e}")

    def toggle_focus_lock(self, instance):
        if "🔒" in self.focus_lock_btn.text:
            self.focus_lock_btn.text = "🔓 Unlock"
            # Enable scrolling
            self.home_scroll.do_scroll_y = True
            self.video_scroll.do_scroll_y = True
            self.blog_scroll.do_scroll_y = True
        else:
            self.focus_lock_btn.text = "🔒 Lock"
            # Disable scrolling
            self.home_scroll.do_scroll_y = False
            self.video_scroll.do_scroll_y = False
            self.blog_scroll.do_scroll_y = False

    def start_timer(self, minutes):
        try:
            requests.get(TIMER_START_URL + str(minutes), timeout=5)
            self.focus_lock_btn.text = "🔒 Lock"  # Auto-lock when timer starts
            self.toggle_focus_lock(None)  # Apply lock
        except:
            self.timer_label.text = "Backend Error"

    def update_timer(self, dt):
        try:
            res = requests.get(TIMER_STATUS_URL, timeout=5).json()

            if res["status"] == "running":
                self.timer_label.text = f"Time Left: {res['remaining']} sec"

            elif res["status"] == "ended":
                self.timer_label.text = "⏰ Timer Ended"
                self.focus_lock_btn.text = "🔓 Unlock"
                self.toggle_focus_lock(None)  # Auto-unlock

            else:
                self.timer_label.text = "No Active Timer"

        except:
            self.timer_label.text = "Backend Offline"

if __name__ == "__main__":
    print("🚀 Starting Productivity App Frontend...")
    ContentApp().run()