
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup


def show_error(message):
    def _popup(dt):
        Popup(
            title="App Error",
            content=Label(text=message),
            size_hint=(0.9, 0.6)
        ).open()
    Clock.schedule_once(_popup)


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
        # By returning nothing or removing this method, 
        # Kivy will look for the root widget defined in your Builder string.
        pass


if __name__ == "__main__":
    try:
        SiloApp().run()
    except Exception as e:
        # This will attempt to show the error on the screen
        # though if the crash is at the 'import' level, this may still fail.
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
