from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import requests

# Your UI Layout
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
            text: "Silo Manager Ready"
            font_size: "20sp"
            halign: "center"

        Button:
            text: "Test Supabase Connection"
            size_hint_y: 0.2
            on_release: app.test_supabase()
"""

class MainScreen(Screen):
    pass

class SiloApp(App):
    # Insert your actual Supabase details here
    SUPABASE_URL = "https://your-project.supabase.co"
    SUPABASE_KEY = "your-anon-key"

    def build(self):
        # We return the Builder result directly to fix the crash
        return Builder.load_string(kv_string)

    def test_supabase(self):
        status = self.root.get_screen('main').ids.status_label
        status.text = "Connecting..."
        
        try:
            headers = {
                "apikey": self.SUPABASE_KEY,
                "Authorization": f"Bearer {self.SUPABASE_KEY}"
            }
            # Change 'inventory' to your actual table name
            response = requests.get(f"{self.SUPABASE_URL}/rest/v1/inventory?select=*", headers=headers, timeout=5)
            
            if response.status_code == 200:
                status.text = "✅ Connection Successful!"
            else:
                status.text = f"❌ Error: {response.status_code}"
        except Exception as e:
            status.text = f"⚠️ Connection Failed"
            print(f"Error: {e}")

if __name__ == "__main__":
    SiloApp().run()
