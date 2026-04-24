#!/usr/bin/env python3
"""
Simple test app to verify Kivy is working
"""
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(text="🎉 Kivy is working!", font_size=24))

        layout.add_widget(Label(text="If you can see this window, Kivy is properly installed!", font_size=16))

        close_btn = Button(text="Close App", size_hint=(1, 0.3), font_size=18)
        close_btn.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(close_btn)

        return layout

if __name__ == "__main__":
    TestApp().run()