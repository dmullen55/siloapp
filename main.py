from kivy.app import App
from kivy.uix.label import Label

class CanaryApp(App):
    def build(self):
        return Label(text="APP BOOTED SUCCESSFULLY ✅")

if __name__ == "__main__":
    CanaryApp().run()
