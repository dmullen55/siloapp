import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder

# ---------------------------------
# SUPABASE REST CONFIG (ANDROID SAFE)
# ---------------------------------

SUPABASE_URL = "https://klhgoevgviqvrihplxxl.supabase.co"
SUPABASE_KEY = "sb_publishable_O41CeFOX5Tb6D-rAFwPPuQ_KS5-ivAH"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def sb_select(table, order=None):
    params = {}
    if order:
        params["order"] = order
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=HEADERS,
        params=params
    )
    return r.json() if r.ok else []

def sb_insert(table, data):
    return requests.post(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=HEADERS,
        json=data
    ).ok

def sb_update(table, col, val, data):
    return requests.patch(
        f"{SUPABASE_URL}/rest/v1/{table}?{col}=eq.{val}",
        headers=HEADERS,
        json=data
    ).ok

def sb_delete(table, col, val):
    return requests.delete(
        f"{SUPABASE_URL}/rest/v1/{table}?{col}=eq.{val}",
        headers=HEADERS
    ).ok

# -----------------
# DATA MODELS
# -----------------

class Silo:
    def __init__(self, silo_id, location, current_material="Empty"):
        self.silo_id = silo_id
        self.location = location
        self.current_material = current_material

class Material:
    def __init__(self, name, po_number, bol_number, mat_type, packaging_type, quantity, unit_label="Units"):
        self.name = name
        self.po_number = po_number
        self.bol_number = bol_number
        self.mat_type = mat_type
        self.packaging_type = packaging_type
        self.quantity = int(quantity)
        self.unit_label = unit_label

    def to_dict(self):
        return self.__dict__

# -----------------
# UI (KIVY)
# -----------------

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
        padding: 20
        spacing: 10

        TextInput:
            id: op
            hint_text: "Operator Name"

        TextInput:
            id: po
            hint_text: "PO Number"

        TextInput:
            id: silo
            hint_text: "Silo ID"

        Button:
            text: "CONFIRM DISCHARGE"
            on_release: root.submit()

        Button:
            text: "BACK"
            on_release: app.root.current = "main"
""")

# -----------------
# SCREENS
# -----------------

class MainScreen(Screen):
    pass

class DischargeScreen(Screen):

    def submit(self):
        app = App.get_running_app()

        po = self.ids.po.text.strip()
        silo = self.ids.silo.text.strip()
        op = self.ids.op.text.strip() or "Unknown"

        mat = next((m for m in app.inventory if m.po_number == po), None)
        sil = next((s for s in app.silos if s.silo_id == silo), None)

        if not mat or not sil:
            self.popup("ERROR", "Invalid PO or Silo")
            return

        sb_insert("inventory_log", {
            "operator": op,
            "po_number": po,
            "silo_id": silo,
            "mat_type": mat.mat_type
        })

        new_qty = max(0, mat.quantity - 1)
        sb_update("inventory", "po_number", po, {"quantity": new_qty})

        app.load_all()
        self.popup("SUCCESS", f"Remaining Qty: {new_qty}")

    def popup(self, title, msg):
        box = BoxLayout(orientation="vertical", padding=10)
        box.add_widget(Label(text=msg))
        btn = Button(text="OK", size_hint_y=None, height=50)
        box.add_widget(btn)
        pop = Popup(title=title, content=box, size_hint=(0.8, 0.4))
        btn.bind(on_release=pop.dismiss)
        pop.open()

# -----------------
# APP
# -----------------

class SiloApp(App):

    inventory = []
    silos = []

    
def build(self):
    return Builder.get_running_app().root


from threading import Thread

def on_start(self):
    Thread(target=self.safe_load_all, daemon=True).start()



    
def safe_load_all(self):
    try:
        self.inventory = [Material(**m) for m in sb_select("inventory")]
        self.silos = [Silo(**s) for s in sb_select("silos", order="silo_id")]
    except Exception as e:
        print("Startup load failed:", e)
        self.inventory = []
        self.silos = []


if __name__ == "__main__":
    SiloApp().run()
