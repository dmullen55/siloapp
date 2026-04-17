from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.label import Label
import requests

# --- CONFIGURATION ---
# Using your verified URL and Key
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
        # Automatically fetch data when the app opens
        self.fetch_silos()

    def fetch_silos(self):
        container = self.root_sm.get_screen('silo_view').ids.silo_container
        container.clear_widgets()
        
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            # Fetching specifically from your 'silos' table
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/silos?select=*", 
                headers=headers, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    container.add_widget(Label(text="No silos found in database.", color=(1, 1, 0, 1)))
                
                for silo in data:
                    silo_id = silo.get('silo_id', 'Unknown')
                    material = silo.get('current_material', 'Empty')
                    location = silo.get('location', 'N/A')
                    
                    # Create a simple display for each silo
                    txt = f"[b]{silo_id}[/b] ({location})\nContent: {material}"
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
                container.add_widget(Label(text=f"Error: {response.status_code}", color=(1, 0, 0, 1)))
                
        except Exception as e:
            container.add_widget(Label(text="Connection Failed", color=(1, 0, 0, 1)))
            print(f"Error: {e}")

if __name__ == "__main__":
    SiloApp().run()
