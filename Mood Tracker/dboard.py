from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout


class MindWave(MDApp):

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.accent_palette = 'Teal'
        return Builder.load_file('dashboard.kv')
    
    class ContentNavigationDrawer(BoxLayout):
        pass



        
MindWave().run()
