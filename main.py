from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import requests

# We define the UI layout here
kv_layout = """
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

        Button:
            text: "Test Supabase Connection"
            size_hint_y: 0.2
            on_release: app.test_supabase()
"""

class MainScreen(Screen):
    pass

class SiloApp(App):
    # Placeholders for your Supabase credentials
    SUPABASE_URL = "https://your-project.supabase.co"
    SUPABASE_KEY = "your-anon-key"

    def build(self):
        # We return the loaded string directly. 
        # This is the "root" of your app.
        return Builder.load_string(kv_layout)

    def test_supabase(self):
        # This function updates the label when you push the button
        status = self.root.get_screen('main').ids.status_label
        status.text = "Attempting Connection..."
        
        try:
            headers = {
                "apikey": self.SUPABASE_KEY,
                "Authorization": f"Bearer {self.SUPABASE_KEY}"
            }
            # Testing against your inventory table
            response = requests.get(f"{self.SUPABASE_URL}/rest/v1/inventory?select=*", headers=headers, timeout=5)
            
            if response.status_code == 200:
                status.text = "✅ Connection Successful!"
            else:
                status.text = f"❌ Error: {response.status_code}"
        except Exception as e:
            status.text = "⚠️ Connection Failed"
            print(f"Error detail: {e}")

if __name__ == "__main__":
    SiloApp().run()
