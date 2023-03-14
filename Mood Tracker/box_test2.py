from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

Builder.load_file('box2.kv')

class MyLayout(Widget):
    pass

class MoodTracker(App):
    def build(self):
        return MyLayout()

if __name__=="__main__":
    MoodTracker().run()