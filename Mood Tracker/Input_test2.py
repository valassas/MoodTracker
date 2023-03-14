import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('MOODTRACKER.kv')

class gridlayout2(Widget):

    name = ObjectProperty(None)
    age = ObjectProperty(None)
    gender = ObjectProperty(None)
    
    def finalize_input(self):
        name = self.name.text
        age = self.age.text
        gender = self.gender.text

        # Show the inputs
        self.add_widget(Label(text =f" Name: {name} Age: {age} Gender: {gender}"))
        
        # Clear the widgets
        self.name.text = ""
        self.age.text = ""
        self.gender.text = ""
        

class MoodTracker(App):
    def build(self):
        return gridlayout2()

if __name__ == '__main__':
    MoodTracker().run()