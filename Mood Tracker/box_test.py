from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

Builder.load_file('box2.kv')

class MyBoxLayout(BoxLayout):
    pass

class BoxLayoutApp(App):
    def build(self):
        return MyBoxLayout()

if __name__=="__main__":
    BoxLayoutApp().run()