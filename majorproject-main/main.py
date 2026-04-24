import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

CONTENT_URL = "http://127.0.0.1:5000/content"
TIMER_START_URL = "http://127.0.0.1:5000/start_timer/"
TIMER_STATUS_URL = "http://127.0.0.1:5000/timer_status"


class ContentApp(App):

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # 🔹 Timer Label
        self.timer_label = Label(
            text="No Timer",
            size_hint=(1, 0.1),
            font_size=20
        )
        self.root.add_widget(self.timer_label)

        # 🔹 Timer Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.1))

        btn_layout.add_widget(Button(text="5 Min", on_press=lambda x: self.start_timer(5)))
        btn_layout.add_widget(Button(text="10 Min", on_press=lambda x: self.start_timer(10)))
        btn_layout.add_widget(Button(text="15 Min", on_press=lambda x: self.start_timer(15)))

        self.root.add_widget(btn_layout)

        # 🔹 Scrollable Content
        self.scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))

        self.scroll.add_widget(self.content_layout)
        self.root.add_widget(self.scroll)

        # 🔹 Load content
        self.load_content()

        # 🔹 Timer update loop
        Clock.schedule_interval(self.update_timer, 1)

        return self.root

    # 📥 Load content
    def load_content(self):
        try:
            response = requests.get(CONTENT_URL)
            data = response.json()

            for item in data:
                title = item.get("title", "No Title")

                label = Label(
                    text=title,
                    size_hint_y=None,
                    height=60
                )
                self.content_layout.add_widget(label)

        except Exception as e:
            self.content_layout.add_widget(Label(text=str(e)))

    # ⏱️ Start timer
    def start_timer(self, minutes):
        try:
            requests.get(TIMER_START_URL + str(minutes))
        except:
            self.timer_label.text = "Server Error"

    # 🔒 Focus Lock Logic
    def apply_focus_lock(self, lock):
        if lock:
            self.scroll.do_scroll_y = False  # Disable scrolling
            self.timer_label.text += " 🔒 Focus Locked"
        else:
            self.scroll.do_scroll_y = True   # Enable scrolling

    # ⏳ Update timer
    def update_timer(self, dt):
        try:
            res = requests.get(TIMER_STATUS_URL).json()

            if res["status"] == "running":
                self.timer_label.text = f"Time Left: {res['remaining']} sec"
                self.apply_focus_lock(True)

            elif res["status"] == "ended":
                self.timer_label.text = "⏰ Timer Ended"
                self.apply_focus_lock(False)

            else:
                self.timer_label.text = "No Active Timer"
                self.apply_focus_lock(False)

        except:
            self.timer_label.text = "Server not running"
            self.apply_focus_lock(False)


if __name__ == "__main__":
    ContentApp().run()