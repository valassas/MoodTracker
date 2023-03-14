import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
#import της παναγιάς τα μάτια

class gridlayout(GridLayout):
    def __init__(self,**kwargs):
        
        # bottom grid layout constructor
        super(gridlayout, self). __init__(**kwargs)
        self.cols = 1
        
        self.row_force_default = True
        self.row_default_height = 100
        self.col_force_default = True
        self.col_default_width = 400
        
        # top grid layout
        self.top_grid = GridLayout(
            row_force_default = True,
            row_default_height = 50,
            col_force_default = True,
            col_default_width = 200)
        self.top_grid.cols =2

        
        # Name Input
        self.top_grid.add_widget(Label(text = "Name: "))
        self.name = TextInput(multiline= False)
        self.top_grid.add_widget(self.name)
        
        # Age Input
        self.top_grid.add_widget(Label(text = "Age: "))
        self.age = TextInput(multiline= False)
        self.top_grid.add_widget(self.age)
        
        # Gender Input
        self.top_grid.add_widget(Label(text = "Gender: "))
        self.gender = TextInput(multiline= False)
        self.top_grid.add_widget(self.gender)
         
        # Add top_grid
        self.add_widget(self.top_grid) 
        
        # Create Submit Button
        self.submit = Button(text = "Submit" ,  
        font_size =24,
        size_hint_y = None,
        height = 50,
        size_hint_x = None,
        width = 400)
        # Bind Button 
        self.submit.bind(on_press=self.finalize_input)
        
        self.add_widget(self.submit)

    def finalize_input(self, instance):
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
        return gridlayout()

if __name__ == '__main__':
    MoodTracker().run()