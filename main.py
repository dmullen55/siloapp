from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import requests # Used for Supabase REST API

kv_string = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10
        
        Label:
            id: status_label
            text: "Checking Connection..."
            font_size: "18sp"
        
        Button:
            text: "Test Supabase Connection"
            size_hint_y: 0.2
            on_release: app.test_connection()
"""

class MainScreen(Screen):
    pass

class SiloApp(App):
    # Replace these with your actual Supabase credentials
    SUPABASE_URL = "https://klhgoevgviqvrihplxxl.supabase.co"
    SUPABASE_KEY = "sb_publishable_O41CeFOX5Tb6D-rAFwPPuQ_KS5-ivAH"

    ddef build(self):
        return Builder.load_string(kv_string)

    def test_connection(self):
        # Moving the import here prevents the app from crashing on startup 
        # if the library is missing.
        try:
            import requests 
            status = self.root.get_screen('main').ids.status_label
            # ... rest of your connection code ...
        except ImportError:
            self.root.get_screen('main').ids.status_label.text = "Missing Requests Library"
