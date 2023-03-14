from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)

        # Set background color
        self.canvas.before.add(Color(rgba=(0.9, 0.9, 0.9, 1)))
        self.canvas.before.add(Rectangle(size=self.size, pos=self.pos))

        # Add widgets
        self.add_widget(Label(text='What is your name?', font_size=40, size_hint_y=None, height=80))
        self.name_input = TextInput(multiline=False, font_size=30, size_hint_y=None, height=60)
        self.add_widget(self.name_input)

        self.add_widget(Label(text='What is your age?', font_size=40, size_hint_y=None, height=80))
        self.age_input = TextInput(multiline=False, font_size=30, size_hint_y=None, height=60)
        self.add_widget(self.age_input)

        self.submit_button = Button(text='Submit', font_size=40, size_hint_y=None, height=80)
        self.submit_button.bind(on_press=self.submit)
        self.add_widget(self.submit_button)

    def submit(self, instance):
        name = self.name_input.text
        age = self.age_input.text
        print(f"Name: {name}, Age: {age}")


class MyApp(App):
    def build(self):
        # Set window size and title
        Window.size = (600, 400)
        Window.title = 'Name and Age'

        # Return main widget
        return MyBoxLayout()


if __name__ == '__main__':
    MyApp().run()
