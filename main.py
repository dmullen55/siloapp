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

    def build(self):
        return Builder.load_string(kv_string)

    def test_connection(self):
        status = self.root.get_screen('main').ids.status_label
        try:
            # Simple GET request to a table (e.g., 'materials' or 'silos')
            headers = {
                "apikey": self.SUPABASE_KEY,
                "Authorization": f"Bearer {self.SUPABASE_KEY}"
            }
            # Change 'your_table_name' to your actual inventory table
            response = requests.get(f"{self.SUPABASE_URL}/rest/v1/your_table_name?select=*", headers=headers, timeout=5)
            
            if response.status_code == 200:
                status.text = "✅ Connected to Supabase!"
                status.color = (0, 1, 0, 1) # Green
            else:
                status.text = f"❌ Error: {response.status_code}"
                status.color = (1, 0, 0, 1) # Red
        except Exception as e:
            status.text = f"⚠️ Connection Failed: {str(e)}"
            status.color = (1, 0, 0, 1)
