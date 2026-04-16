from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

# We define the UI string first
kv_string = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "✅ SILO MANAGER LOADED"
            font_size: "22sp"
"""

class MainScreen(Screen):
    pass

class SiloApp(App):
    def build(self):
        # We return the loaded string directly. 
        # This prevents the 'NoneType' or 'Double Root' crash.
        return Builder.load_string(kv_string)

if __name__ == "__main__":
    SiloApp().run()
