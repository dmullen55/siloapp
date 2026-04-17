import requests
import certifi
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.label import Label

# --- CONFIGURATION ---
# Verified URL and Key
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
        # Small delay to ensure network is ready on the phone
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.fetch_silos(), 1)

    def fetch_silos(self):
        container = self.root_sm.get_screen('silo_view').ids.silo_container
        container.clear_widgets()
        container.add_widget(Label(text="Connecting to Database...", color=(0.5, 0.5, 0.5, 1)))
        
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            }
            
            # Using verify=certifi.where() is mandatory for Android requests to Supabase
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/silos?select=*", 
                headers=headers, 
                timeout=15,
                verify=certifi.where()
            )
            
            container.clear_widgets()
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    container.add_widget(Label(text="Success: Table is Empty", color=(1, 1, 1, 1)))
                
                for silo in data:
                    s_id = silo.get('silo_id', 'Unknown')
                    mat = silo.get('current_material', 'Empty')
                    txt = f"[b]{s_id}[/b]\\n{mat}"
                    lbl = Label(text=txt, markup=True, size_hint_y=None, height="80dp", halign="center")
                    lbl.bind(size=lbl.setter('text_size'))
                    container.add_widget(lbl)
            else:
                container.add_widget(Label(text=f"HTTP {response.status_code}: Access Denied", color=(1, 0.5, 0, 1)))
                
        except Exception as e:
            container.clear_widgets()
            # This captures the specific nature of the HTTPSConnectionPool error
            raw_err = str(e)
            if "Certificate" in raw_err or "SSL" in raw_err:
                msg = "SSL/Security Error"
            elif "Failed to establish" in raw_err:
                msg = "No Internet/Server Down"
            else:
                msg = raw_err[:45]
            container.add_widget(Label(text=f"ERROR:\\n{msg}", color=(1, 0, 0, 1), halign="center"))

if __name__ == "__main__":
    SiloApp().run()
