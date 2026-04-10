import requests
import certifi
import traceback
from threading import Thread

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock

# ----------------------
# SUPABASE CONFIG
# ----------------------
SUPABASE_URL = "https://klhgoevgviqvrihplxxl.supabase.co"
SUPABASE_KEY = "sb_publishable_O41CeFOX5Tb6D-rAFwPPuQ_KS5-ivAH"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ----------------------
# SUPABASE HELPERS
# ----------------------
def sb_select(table, order=None):
    params = {}
    if order:
        params["order"] = order
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=HEADERS,
        params=params,
        verify=certifi.where()
    )
    return r.json() if r.ok else []

# ----------------------
# ERROR DISPLAY (ANDROID SAFE)
# ----------------------
def show_error(message):
    def _popup(dt):
        Popup(
            title="App Error",
            content=Label(text=message),
            size_hint=(0.9, 0.6)
        ).open()
    Clock.schedule_once(_popup)

# ----------------------
# DATA MODELS
# ----------------------
class Silo:
    def __init__(self, silo_id, location, current_material="Empty"):
        self.silo_id = silo_id
        self.location = location
        self.current_material = current_material

class Material:
    def __init__(self, name, po_number, bol_number, mat_type,
                 packaging_type, quantity, unit_label="Units"):
        self.name = name
        self.po_number = po_number
        self.bol_number = bol_number
        self.mat_type = mat_type
        self.packaging_type = packaging_type
        self.quantity = int(quantity)
        self.unit_label = unit_label

# ----------------------
# UI (KV)
# ----------------------
Builder.load_string("""
ScreenManager:
    MainScreen:
    DischargeScreen:

<MainScreen>:
    name: "main"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "SILO MANAGEMENT"
            font_size: "24sp"
        Button:
            text: "START DISCHARGE"
            on_release: app.root.current = "discharge"

<DischargeScreen>:
    name: "discharge"
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "Discharge Screen"
""")

class MainScreen(Screen):
    pass

class DischargeScreen(Screen):
    pass

# ----------------------
# APP
# ----------------------
class SiloApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(DischargeScreen())
        return sm

    def on_start(self):
        Thread(target=self.safe_load_all, daemon=True).start()

    def safe_load_all(self):
        try:
            self.inventory = [Material(**m) for m in sb_select("inventory")]
            self.silos = [Silo(**s) for s in sb_select("silos", order="silo_id")]
        except Exception:
            err = traceback.format_exc()
            print(err)
            show_error(err)

if __name__ == "__main__":
    SiloApp().run()
