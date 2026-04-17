import os
from datetime import datetime
from supabase import create_client, Client

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from kivy.core.window import Window

# --- CONFIGURATION ---
SUPABASE_URL = "https://klhgoevgviquvrihplxxl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtsaGdvZXZndmlxdnJpaHBseHhsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM0MjIxNDcsImV4cCI6MjA4ODk5ODE0N30.FqsZBtKnSrZx06Z6RdZ75zyRqD5-0mZXQp7TeGYEa0I"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Supabase Connection Error: {e}")

# --- DATA MODELS ---
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
        self.quantity = int(float(quantity))
        self.unit_label = unit_label
    def to_dict(self): return self.__dict__

# --- UI DESIGN (KV STRING) ---
kv_string = """
<HeaderLabel@Label>:
    font_size: '20sp'
    bold: True
    size_hint_y: None
    height: '70dp'
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<FieldLabel@Label>:
    size_hint_y: None
    height: '30dp'
    font_size: '14sp'
    halign: 'left'
    bold: True
    color: (0.8, 0.8, 0.8, 1)

<MenuButton@Button>:
    font_size: '16sp'
    size_hint_y: None
    height: '60dp'
    background_color: (0.1, 0.5, 0.8, 1)

<FooterButton@Button>:
    size_hint_y: None
    height: '60dp'
    background_color: (0.3, 0.3, 0.3, 1)

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'SILO MANAGEMENT'
        BoxLayout:
            orientation: 'vertical'
            padding: 30
            spacing: 20
            MenuButton:
                text: 'START DISCHARGE SCAN'
                background_color: (0.2, 0.6, 0.3, 1)
                on_release: root.manager.current = 'discharge'
            MenuButton:
                text: 'VIEW SILO STATUS'
                on_release: root.manager.current = 'silo_view'
            Widget:
            MenuButton:
                text: 'ADMIN LOGIN'
                on_release: root.manager.current = 'login'

<SuccessLogScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'SUCCESSFUL DISCHARGES'
        ScrollView:
            GridLayout:
                id: log_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 5
        FooterButton:
            text: 'BACK'
            on_release: root.manager.current = 'admin_menu'

<FailureLogScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'FAILURE REPORTS'
        ScrollView:
            GridLayout:
                id: fail_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 5
        FooterButton:
            text: 'BACK'
            on_release: root.manager.current = 'admin_menu'

<DischargeScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'DISCHARGE SCAN'
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 10
                size_hint_y: None
                height: self.minimum_height
                FieldLabel: 
                    text: 'OPERATOR NAME:'
                TextInput:
                    id: op_name
                    multiline: False
                    size_hint_y: None
                    height: '50dp'
                FieldLabel: 
                    text: 'SCAN OR TYPE PO:'
                TextInput:
                    id: po_input
                    on_text: root.check_po_live(self.text)
                    multiline: False
                    size_hint_y: None
                    height: '50dp'
                BoxLayout:
                    id: loaded_info_box
                    orientation: 'vertical'
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    canvas.before:
                        Color:
                            rgba: (0.2, 0.2, 0.2, 1)
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    Label:
                        id: loaded_po_display
                        text: ''
                        bold: True
                    Label:
                        id: loaded_mat_display
                        text: ''
                        color: (0.2, 0.8, 1, 1)
                FieldLabel: 
                    text: 'SCAN OR TYPE SILO:'
                TextInput:
                    id: silo_input
                    disabled: True
                    on_text: root.check_silo_live(self.text)
                    size_hint_y: None
                    height: '50dp'
                Button:
                    id: confirm_btn
                    text: 'CONFIRM DISCHARGE'
                    background_color: (0.2, 0.8, 0.2, 1)
                    size_hint_y: None
                    height: 0
                    opacity: 0
                    disabled: True
                    on_release: root.finalize_discharge()
                Label:
                    id: status_msg
                    text: 'Awaiting Operator & PO...'
                    color: (1, 1, 0, 1)
                    text_size: self.width, None
                    halign: 'center'
                    bold: True
        BoxLayout:
            size_hint_y: None
            height: '60dp'
            FooterButton:
                text: 'RESET'
                on_release: root.reset()
            FooterButton:
                text: 'BACK'
                on_release: root.manager.current = 'main'

<AdminSiloListScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel: 
            text: 'EDIT SILO CONTENTS'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: 'INSIDE'
                on_release: root.load_view("Inside")
            Button:
                text: 'OUTSIDE'
                on_release: root.load_view("Outside")
        ScrollView:
            GridLayout:
                id: admin_silo_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 10
        FooterButton:
            text: 'BACK'
            on_release: root.manager.current = 'admin_menu'

<EditMaterialScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'EDIT MATERIAL'
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 5
                size_hint_y: None
                height: self.minimum_height
                FieldLabel:
                    text: 'DESCRIPTION:'
                TextInput:
                    id: m_name
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'PO NUMBER (Locked):'
                TextInput:
                    id: m_po
                    disabled: True
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'BOL NUMBER:'
                TextInput:
                    id: m_bol
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'MATERIAL GRADE:'
                Spinner:
                    id: m_type
                    text: 'Select Grade'
                    values: root.get_mat_list()
                    size_hint_y: None
                    height: '45dp'
                FieldLabel:
                    text: 'PACKAGING:'
                Spinner:
                    id: m_packaging
                    text: 'Super Sacks'
                    values: ['Super Sacks', 'Boxes', 'Compartments']
                    size_hint_y: None
                    height: '45dp'
                FieldLabel:
                    text: 'QUANTITY (Whole Units):'
                TextInput:
                    id: m_qty
                    input_filter: 'int'
                    size_hint_y: None
                    height: '40dp'
        BoxLayout:
            size_hint_y: None
            height: '65dp'
            FooterButton:
                text: 'UPDATE'
                background_color: (0.1, 0.6, 0.1, 1)
                on_release: root.update_data()
            FooterButton:
                text: 'DELETE'
                background_color: (0.8, 0.1, 0.1, 1)
                on_release: root.confirm_delete_popup()
            FooterButton:
                text: 'CANCEL'
                on_release: root.manager.current = 'inventory_view'

<AddMaterialScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'ADD NEW MATERIAL'
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 5
                size_hint_y: None
                height: self.minimum_height
                FieldLabel:
                    text: 'DESCRIPTION:'
                TextInput:
                    id: m_name
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'PO NUMBER:'
                TextInput:
                    id: m_po
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'BOL NUMBER:'
                TextInput:
                    id: m_bol
                    size_hint_y: None
                    height: '40dp'
                FieldLabel:
                    text: 'MATERIAL GRADE:'
                Spinner:
                    id: m_type
                    text: 'Select Grade'
                    values: root.get_mat_list()
                    size_hint_y: None
                    height: '45dp'
                FieldLabel:
                    text: 'PACKAGING:'
                Spinner:
                    id: m_packaging
                    text: 'Super Sacks'
                    values: ['Super Sacks', 'Boxes', 'Compartments']
                    size_hint_y: None
                    height: '45dp'
                FieldLabel:
                    text: 'QUANTITY (Whole Units):'
                TextInput:
                    id: m_qty
                    input_filter: 'int'
                    size_hint_y: None
                    height: '40dp'
        BoxLayout:
            size_hint_y: None
            height: '65dp'
            FooterButton:
                text: 'SAVE'
                on_release: root.save_data()
            FooterButton:
                text: 'CANCEL'
                on_release: root.manager.current = 'inventory_view'

<InventoryScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'INVENTORY'
        Label:
            text: 'Click item to edit'
            size_hint_y: None
            height: '30dp'
            color: (0.6, 0.6, 0.6, 1)
            font_size: '12sp'
        ScrollView:
            GridLayout:
                id: inv_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 10
                spacing: 10
        BoxLayout:
            size_hint_y: None
            height: '65dp'
            FooterButton:
                text: 'ADD NEW'
                on_release: root.manager.current = 'add_material'
            FooterButton:
                text: 'BACK'
                on_release: root.manager.current = 'admin_menu'

<SiloScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'SILO STATUS'
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: 'INSIDE'
                on_release: root.load_filtered_view("Inside")
            Button:
                text: 'OUTSIDE'
                on_release: root.load_filtered_view("Outside")
        ScrollView:
            GridLayout:
                id: silo_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: 15
                spacing: 10
        FooterButton:
            text: 'BACK'
            on_release: root.manager.current = 'main'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'ADMIN LOGIN'
        BoxLayout:
            orientation: 'vertical'
            padding: 50
            spacing: 20
            FieldLabel:
                text: 'PIN:'
            TextInput:
                id: pass_input
                password: True
                size_hint_y: None
                height: '50dp'
            Button:
                text: 'ENTER'
                on_release: root.verify_password()
            Widget:
        FooterButton:
            text: 'BACK'
            on_release: root.manager.current = 'main'

<AdminMenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        HeaderLabel:
            text: 'ADMIN CONTROL'
        BoxLayout:
            orientation: 'vertical'
            padding: 30
            spacing: 12
            MenuButton:
                text: 'MANAGE INVENTORY'
                on_release: root.manager.current = 'inventory_view'
            MenuButton:
                text: 'EDIT SILO CONTENTS'
                on_release: root.manager.current = 'admin_silo_list'
            MenuButton:
                text: 'SUCCESSFUL DISCHARGES'
                background_color: (0.2, 0.4, 0.6, 1)
                on_release: root.manager.current = 'success_logs'
            MenuButton:
                text: 'FAILURE REPORTS'
                background_color: (0.7, 0.3, 0.2, 1)
                on_release: root.manager.current = 'failure_logs'
            Widget:
        FooterButton:
            text: 'LOGOUT'
            on_release: root.manager.current = 'main'
"""

class MaterialListMixin:
    def get_mat_list(self):
        return [
            "258141 - 8M HDPE VIRGIN", "257341 - 8M HDPE REGRIND", "568691 - 8M HDPE PELLETIZED", 
            "258159 - 5M HDPE VIRGIN", "257359 - 5M HDPE REGRIND", "544542 - 5M HDPE PELLETIZED", 
            "531995 - WIDE SPEC HDPE", "258183 - 20M PP VIRGIN", "257375 - 20M PP REGRIND", 
            "568739 - 20M PP PELLETIZED", "258175 - 5M PP VIRGIN", "257367 - 5M PP REGRIND", 
            "568721 - 5M PP PELLETIZED", "257332 - FRAC", "568704 - VIRGIN FRAC", 
            "517464 - BULKY RIGID", "257383 - TPE", "288067 - PURGE", 
            "257391 - GENERIC REGRIND", "288059 - HDPE FINES/DUST"
        ]

# --- SCREEN CLASSES ---
class MainScreen(Screen): pass
class AdminMenuScreen(Screen): pass

class SuccessLogScreen(Screen):
    def on_enter(self):
        self.ids.log_list.clear_widgets()
        try:
            res = supabase.table("inventory_log").select("*").order("timestamp", desc=True).limit(50).execute()
            for entry in res.data:
                txt = f"[b]{entry['timestamp'][:16].replace('T', ' ')}[/b]\nOp: {entry['operator']} | Silo: {entry['silo_id']}\nPO: {entry['po_number']} ({entry['mat_type']})"
                lbl = Label(text=txt, markup=True, size_hint_y=None, height=100, font_size='12sp', halign='left')
                lbl.bind(size=lbl.setter('text_size'))
                self.ids.log_list.add_widget(lbl)
        except: pass

class FailureLogScreen(Screen):
    def on_enter(self):
        self.ids.fail_list.clear_widgets()
        try:
            res = supabase.table("failed_scans").select("*").order("timestamp", desc=True).limit(50).execute()
            for entry in res.data:
                txt = f"[b][color=ff3333]{entry['failure_reason'].upper()}[/color][/b] - {entry['timestamp'][:16].replace('T', ' ')}\nOp: {entry['operator']} | Silo Attempted: {entry['silo_id']}\nPO: {entry['po_number']}"
                lbl = Label(text=txt, markup=True, size_hint_y=None, height=100, font_size='12sp', halign='left')
                lbl.bind(size=lbl.setter('text_size'))
                self.ids.fail_list.add_widget(lbl)
        except: pass

class DischargeScreen(Screen):
    def on_enter(self): self.reset()

    def reset(self):
        self.selected_mat = None
        self.selected_silo = None
        self.ids.po_input.text = ""
        self.ids.po_input.disabled = False
        self.ids.silo_input.text = ""
        self.ids.silo_input.disabled = True
        self.ids.status_msg.text = "Scan or Type PO Number"
        self.ids.status_msg.color = (1, 1, 0, 1)
        self.ids.loaded_info_box.height = 0
        self.ids.loaded_info_box.opacity = 0
        self.ids.confirm_btn.height = 0
        self.ids.confirm_btn.opacity = 0
        self.ids.confirm_btn.disabled = True

    def log_failure(self, reason, silo_id="Unknown"):
        fail_data = {
            "operator": self.ids.op_name.text or "Unknown",
            "po_number": self.selected_mat.po_number if self.selected_mat else "None",
            "silo_id": silo_id,
            "failure_reason": reason,
            "mat_type": self.selected_mat.mat_type if self.selected_mat else "None"
        }
        try: supabase.table("failed_scans").insert(fail_data).execute()
        except: pass

    def trigger_error_popup(self, title, message):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        lbl = Label(text=message, halign='center', valign='middle')
        lbl.bind(size=lbl.setter('text_size'))
        btn = Button(text="OK", size_hint=(1, 0.4), background_color=(0.8, 0.2, 0.2, 1))
        layout.add_widget(lbl)
        layout.add_widget(btn)
        popup = Popup(title=title, content=layout, size_hint=(0.8, 0.45), auto_dismiss=False)
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def check_po_live(self, text):
        app = App.get_running_app()
        clean_input = text.strip().replace("PO:", "").strip().upper()
        mat = next((m for m in app.inventory if str(m.po_number).strip().upper() == clean_input), None)
        if mat:
            self.selected_mat = mat
            self.ids.po_input.disabled = True
            self.ids.silo_input.disabled = False
            self.ids.loaded_info_box.height = 70
            self.ids.loaded_info_box.opacity = 1
            self.ids.loaded_po_display.text = f"LOADED PO: {mat.po_number}"
            self.ids.loaded_mat_display.text = mat.mat_type
            self.ids.status_msg.text = "PO Verified. Scan Silo QR."
            self.ids.status_msg.color = (0, 1, 0, 1)
            self.ids.silo_input.focus = True

    def check_silo_live(self, text):
        app = App.get_running_app()
        s_id_scanned = text.strip().replace("SILO:", "").strip().upper()
        silo = next((s for s in app.silos if s.silo_id.replace(" ", "").upper() == s_id_scanned.replace(" ", "").upper()), None)
        
        if silo and self.selected_mat:
            def deep_clean(val): return "".join(filter(str.isalnum, val)).upper()
            silo_contents = [deep_clean(g) for g in silo.current_material.split(" | ")]
            po_grade = deep_clean(self.selected_mat.mat_type)
            
            if "EMPTY" in silo_contents:
                self.log_failure("Silo Empty", silo.silo_id)
                self.trigger_error_popup("SILO EMPTY", f"Silo {silo.silo_id} is currently set to Empty.")
                self.ids.silo_input.text = ""
                return
            
            if po_grade in silo_contents:
                self.selected_silo = silo
                self.ids.silo_input.disabled = True
                self.ids.confirm_btn.height = '60dp'
                self.ids.confirm_btn.opacity = 1
                self.ids.confirm_btn.disabled = False
                self.ids.status_msg.text = "GRADE MATCHED! Press Confirm."
                self.ids.status_msg.color = (0, 1, 1, 1)
            else:
                self.log_failure("Grade Mismatch", silo.silo_id)
                msg = (f"GRADE MISMATCH\n\nPO Grade: {self.selected_mat.mat_type}\n"
                       f"Silo Allows: {silo.current_material}")
                self.trigger_error_popup("VERIFICATION FAILED", msg)
                self.ids.silo_input.text = ""

    def finalize_discharge(self):
        if not self.selected_silo or not self.selected_mat: return
        app = App.get_running_app()
        log_data = {
            "operator": self.ids.op_name.text or "Unknown", 
            "po_number": self.selected_mat.po_number, 
            "silo_id": self.selected_silo.silo_id, 
            "mat_type": self.selected_mat.mat_type
        }
        try:
            supabase.table("inventory_log").insert(log_data).execute()
            new_qty = max(0, int(self.selected_mat.quantity) - 1)
            supabase.table("inventory").update({"quantity": new_qty}).eq("po_number", self.selected_mat.po_number).execute()
            app.load_all()
            self.reset()
            self.ids.status_msg.text = f"SUCCESS! REMAINING: {new_qty}"
            self.ids.status_msg.color = (0, 1, 0, 1)
        except Exception as e:
            self.ids.status_msg.text = "Database Error"

class AdminSiloListScreen(Screen, MaterialListMixin):
    def on_enter(self): self.load_view("Inside")
    def load_view(self, loc):
        self.ids.admin_silo_grid.clear_widgets()
        app = App.get_running_app()
        for s in app.silos:
            if s.location == loc:
                display_text = s.current_material.replace(" | ", "\n• ")
                btn = Button(text=f"[b]{s.silo_id}[/b]\n• {display_text}", markup=True, size_hint_y=None, height=120)
                btn.bind(on_release=lambda x, silo=s: self.edit_popup(silo))
                self.ids.admin_silo_grid.add_widget(btn)

    def edit_popup(self, silo):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll = ScrollView(size_hint=(1, 0.7))
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        current_selections = silo.current_material.split(" | ")
        grade_buttons = []
        def toggle_grade(btn):
            if btn.text == "Empty":
                for b in grade_buttons: 
                    if b.text != "Empty": b.state = 'normal'
            else:
                for b in grade_buttons:
                    if b.text == "Empty": b.state = 'normal'
        grades = ["Empty"] + self.get_mat_list()
        for g in grades:
            is_active = 'down' if g in current_selections else 'normal'
            btn = ToggleButton(text=g, state=is_active, size_hint_y=None, height=45)
            btn.bind(on_release=toggle_grade)
            grade_buttons.append(btn)
            grid.add_widget(btn)
        scroll.add_widget(grid)
        layout.add_widget(Label(text=f"Assign Grades to {silo.silo_id}", size_hint_y=None, height=30))
        layout.add_widget(scroll)
        save_btn = Button(text="Save Update", size_hint_y=None, height=50, background_color=(0, 0.7, 0, 1))
        layout.add_widget(save_btn)
        pop = Popup(title="Assign Hierarchy", content=layout, size_hint=(0.9, 0.8))
        def update(instance):
            selected = [b.text for b in grade_buttons if b.state == 'down']
            new_val = " | ".join(selected) if selected else "Empty"
            try:
                supabase.table("silos").update({"current_material": new_val}).eq("silo_id", silo.silo_id).execute()
                App.get_running_app().load_all()
                self.load_view(silo.location)
                pop.dismiss()
            except: pass
        save_btn.bind(on_release=update)
        pop.open()

class EditMaterialScreen(Screen, MaterialListMixin):
    target_po = None
    def on_pre_enter(self):
        app = App.get_running_app()
        mat = next((m for m in app.inventory if m.po_number == self.target_po), None)
        if mat:
            self.ids.m_name.text = str(mat.name)
            self.ids.m_po.text = str(mat.po_number)
            self.ids.m_bol.text = str(mat.bol_number)
            self.ids.m_type.text = str(mat.mat_type)
            self.ids.m_packaging.text = str(mat.packaging_type)
            self.ids.m_qty.text = str(int(mat.quantity))

    def update_data(self):
        data = {
            "name": self.ids.m_name.text, 
            "bol_number": self.ids.m_bol.text, 
            "mat_type": self.ids.m_type.text, 
            "packaging_type": self.ids.m_packaging.text, 
            "quantity": int(float(self.ids.m_qty.text or 0))
        }
        try:
            supabase.table("inventory").update(data).eq("po_number", self.target_po).execute()
            App.get_running_app().load_all()
            self.manager.current = 'inventory_view'
        except: pass

    def confirm_delete_popup(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        lbl = Label(text=f"Permanently delete PO {self.target_po}?", halign='center')
        lbl.bind(size=lbl.setter('text_size'))
        btn_box = BoxLayout(spacing=10, size_hint_y=None, height='50dp')
        yes_btn = Button(text="DELETE", background_color=(0.8, 0.1, 0.1, 1))
        no_btn = Button(text="CANCEL", background_color=(0.3, 0.3, 0.3, 1))
        btn_box.add_widget(yes_btn); btn_box.add_widget(no_btn)
        layout.add_widget(lbl); layout.add_widget(btn_box)
        pop = Popup(title="Confirm Deletion", content=layout, size_hint=(0.8, 0.4))
        def do_delete(instance):
            try:
                supabase.table("inventory").delete().eq("po_number", self.target_po).execute()
                App.get_running_app().load_all()
                pop.dismiss()
                self.manager.current = 'inventory_view'
            except: pass
        no_btn.bind(on_release=pop.dismiss); yes_btn.bind(on_release=do_delete); pop.open()

class AddMaterialScreen(Screen, MaterialListMixin):
    def save_data(self):
        m_qty_clean = int(float(self.ids.m_qty.text or 0))
        m = Material(
            self.ids.m_name.text, 
            self.ids.m_po.text, 
            self.ids.m_bol.text, 
            self.ids.m_type.text, 
            self.ids.m_packaging.text, 
            m_qty_clean
        )
        try:
            supabase.table("inventory").insert(m.to_dict()).execute()
            App.get_running_app().load_all()
            self.manager.current = 'inventory_view'
        except: pass

class SiloScreen(Screen):
    def load_filtered_view(self, loc):
        self.ids.silo_list.clear_widgets()
        app = App.get_running_app()
        for s in app.silos:
            if s.location == loc:
                clean_list = s.current_material.replace(" | ", "\n• ")
                txt = f"[b]{s.silo_id}[/b]\n• {clean_list}"
                lbl = Label(text=txt, markup=True, size_hint_y=None, height=140, halign='left', valign='middle')
                lbl.bind(size=lbl.setter('text_size'))
                self.ids.silo_list.add_widget(lbl)

class InventoryScreen(Screen):
    def on_enter(self):
        self.ids.inv_list.clear_widgets()
        for item in App.get_running_app().inventory:
            btn = Button(text=f"PO: {item.po_number} | Qty: {int(item.quantity)} | {item.mat_type}", size_hint_y=None, height=60)
            btn.bind(on_release=lambda x, po=item.po_number: self.open_edit(po))
            self.ids.inv_list.add_widget(btn)
    def open_edit(self, po):
        self.manager.get_screen('edit_material').target_po = po
        self.manager.current = 'edit_material'

class LoginScreen(Screen):
    def verify_password(self):
        if self.ids.pass_input.text == "1234": self.manager.current = 'admin_menu'
        self.ids.pass_input.text = ""

# --- MAIN APP CLASS ---
class SiloApp(App):
    inventory = []
    silos = []
    
    def build(self):
        self.load_all()
        # We load the KV string here
        Builder.load_string(kv_string)
        
        # We build the ScreenManager manually to ensure proper initialization on Android
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SuccessLogScreen(name='success_logs'))
        sm.add_widget(FailureLogScreen(name='failure_logs'))
        sm.add_widget(DischargeScreen(name='discharge'))
        sm.add_widget(SiloScreen(name='silo_view'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminMenuScreen(name='admin_menu'))
        sm.add_widget(InventoryScreen(name='inventory_view'))
        sm.add_widget(AdminSiloListScreen(name='admin_silo_list'))
        sm.add_widget(AddMaterialScreen(name='add_material'))
        sm.add_widget(EditMaterialScreen(name='edit_material'))
        return sm
        
    def load_all(self):
        try:
            self.silos = [Silo(**s) for s in supabase.table("silos").select("*").order("silo_id").execute().data]
            self.inventory = [Material(**m) for m in supabase.table("inventory").select("*").execute().data]
        except Exception as e:
            print(f"Data Fetch Error: {e}")

if __name__ == "__main__":
    SiloApp().run()
