from kivy.lang import Builder
from kivymd.app import MDApp

class APP(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.accent_palette = 'BlueGray'
        return Builder.load_file('color_theme.kv')
    
    def log(self):
        if (self.root.ids.user.text != "" and self.root.ids.password.text != ""):
            self.root.ids.greet.text = "Επιτυχής Σύνδεση"
        else:
            pass
    
    def clear(self):
        self.root.ids.user.text = ""
        self.root.ids.password.text = ""
        self.root.ids.greet.text = "Επιτυχής Εκκαθάριση"

APP().run()