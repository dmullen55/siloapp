from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.popup import Popup

# ---------------------------
# VERY SAFE ERROR POPUP
# ---------------------------
def show_error(message):
    def _popup(dt):
        Popup(
            title="App Error",
            content=Label(text=message),
            size_hint=(0.9, 0.6)
        ).open()
    Clock.schedule_once(_popup)


# ---------------------------
# KV (MINIMAL & VALID)
# ---------------------------
Builder.load_string("""
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "✅ APP LOADED"
            font_size: "22sp"
""")


class MainScreen(Screen):
    pass


class SiloApp(App):

    def build(self):
        Logger.info("APP: build() called")
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        return sm

    def on_start(self):
        Logger.info("APP: on_start() called")
        Clock.schedule_once(self.safe_post_start, 1)

    def safe_post_start(self, dt):
        Logger.info("APP: app stable, no crash")


if __name__ == "__main__":
    SiloApp().run()
``
