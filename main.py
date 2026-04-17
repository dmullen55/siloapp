import requests
import certifi
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.clock import Clock

# --- CONFIGURATION ---
# Note the 'u' in 'viquvrihplxxl' - this must be exact
SUPABASE_URL = "https://klhgoevgviquvrihplxxl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtsaGdvZXZndmlxdnJpaHBseHhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MjIxNDcsImV4cCI6MjA4ODk5ODE0N30.FqsZBtKnSrZx06Z6RdZ75zyRqD5-0mZXQp7TeGYEa0I"

kv_string = """
ScreenManager:
    SiloViewScreen:

<SiloViewScreen>:
    name: "silo_view"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 10
        Label:
            text: "SILO STATUS"
            font_size: "24sp"
            size_hint_y: None
            height: "60dp"
        ScrollView:
            GridLayout:
                id: silo_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
        Button:
            text: "REFRESH"
            size_hint_y: None
            height: "60dp"
            on_release: app.fetch_silos()
"""

class SiloViewScreen(Screen):
    pass

class SiloApp(App):
    def build(self):
        return Builder.load_string(kv_string)

    def on_start(self):
        Clock.schedule_once(lambda dt: self.fetch_silos(), 1)

    def fetch_silos(self):
        container = self.root.get_screen('silo_view').ids.silo_container
        container.clear_widgets()
        container.add_widget(Label(text="Connecting..."))
        
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            # Using verify=certifi.where() handles the SSL handshake
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/silos?select=*", 
                headers=headers, 
                timeout=10,
                verify=certifi.where()
            )
            
            container.clear_widgets()
            if response.status_code == 200:
                data = response.json()
                for silo in data:
                    s_id = silo.get('silo_id', 'Unknown')
                    mat = silo.get('current_material', 'Empty')
                    container.add_widget(Label(text=f"{s_id}: {mat}", size_hint_y=None, height="50dp"))
            else:
                container.add_widget(Label(text=f"Error {response.status_code}"))
        except Exception as e:
            container.add_widget(Label(text=f"Fail: {str(e)[:30]}"))

if __name__ == "__main__":
    SiloApp().run()
