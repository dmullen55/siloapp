import requests
import certifi
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.label import Label

# --- CONFIGURATION ---
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
            bold: True
            size_hint_y: None
            height: "60dp"
            
        ScrollView:
            GridLayout:
                id: silo_container
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 10
                padding: 10

        Button:
            text: "REFRESH SILO DATA"
            size_hint_y: None
            height: "60dp"
            on_release: app.fetch_silos()
"""

class SiloViewScreen(Screen):
    pass

class SiloApp(App):
    def build(self):
        self.root_sm = Builder.load_string(kv_string)
        return self.root_sm

    def on_start(self):
        self.fetch_silos()

    def fetch_silos(self):
        container = self.root_sm.get_screen('silo_view').ids.silo_container
        container.clear_widgets()
        
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            # Adding verify=certifi.where() for Android SSL stability
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/silos?select=*", 
                headers=headers, 
                timeout=10,
                verify=certifi.where()
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    container.add_widget(Label(text="No silos found.", color=(1, 1, 0, 1)))
                
                for silo in data:
                    s_id = silo.get('silo_id', 'Unknown')
                    mat = silo.get('current_material', 'Empty')
                    loc = silo.get('location', 'N/A')
                    
                    txt = f"[b]{s_id}[/b] ({loc})\\nContent: {mat}"
                    lbl = Label(
                        text=txt, 
                        markup=True, 
                        size_hint_y=None, 
                        height="80dp",
                        halign="left"
                    )
                    lbl.bind(size=lbl.setter('text_size'))
                    container.add_widget(lbl)
            else:
                container.add_widget(Label(text=f"HTTP Error: {response.status_code}", color=(1, 0, 0, 1)))
                
        except Exception as e:
            # Show the actual error on screen for easier debugging
            err_text = str(e)[:40]
            container.add_widget(Label(text=f"Error: {err_text}", color=(1, 0, 0, 1)))

if __name__ == "__main__":
    SiloApp().run()
