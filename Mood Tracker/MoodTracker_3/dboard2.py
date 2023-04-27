from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
import numpy as np
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
# The warning (Yellow squiggles) does not affect anything. Everything works as it should
import matplotlib.pyplot as plt
from kivy.uix.floatlayout import FloatLayout
import numpy as np
from matplotlib import pyplot as plt
import sys
import json
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.navigationdrawer import MDNavigationDrawerMenu
import datetime
import random
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.checkbox import CheckBox


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class QuizWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Create the quiz questions
        self.questions = [
            "How are you feeling today?",
            "Did you get enough sleep last night?",
            "Have you eaten a healthy meal today?",
            "Have you exercised today?"
        ]

        # Create the answer options for each question
        self.answers = [
            ["Great", "Good", "Okay", "Not so good", "Terrible"],
            ["Yes", "No"],
            ["Yes", "No"],
            ["Yes", "No"]
        ]

        # Create a dictionary to store the user's answers
        self.user_answers = {}

        # Create the quiz labels and answer checkboxes
        self.quiz_labels = []
        self.quiz_checkboxes = []
        for i, question in enumerate(self.questions):
            self.quiz_labels.append(MDLabel(text=question))
            self.add_widget(self.quiz_labels[-1])
            for answer in self.answers[i]:
                checkbox = CheckBox(group=str(i))
                checkbox.answer = answer
                checkbox.bind(active=self.on_answer)
                self.quiz_checkboxes.append(checkbox)
                self.add_widget(checkbox)
                self.add_widget(MDLabel(text=answer))

            # Add a separator between questions
            separator = MDLabel(text="--------------------------------------------------")
            self.add_widget(separator)

        # Create the submit button
        self.submit_button = MDFillRoundFlatButton(text="Finish Quiz", on_press=self.on_submit)
        self.submit_button.disabled = True
        self.add_widget(self.submit_button)

        # Create the advice label, but hide it initially
        self.advice_label = MDLabel(text="")
        self.add_widget(self.advice_label)
        self.advice_label.opacity = 0
    
    def on_answer(self, checkbox, is_active):
        # Store the user's answer in the dictionary
        question_index = int(checkbox.group)
        answer = checkbox.answer
        self.user_answers[question_index] = answer

        # Enable the submit button if all questions have been answered
        if len(self.user_answers) == len(self.questions):
            self.submit_button.disabled = False

    def on_submit(self, button):
        # Calculate the score based on the user's answers
        score = 0
        for answer in self.user_answers.values():
            if answer in ["Great", "Yes"]:
                score += 1

        # Provide advice based on the score
        if score == len(self.questions):
            self.advice_label.text = "You're doing great! Keep it up!"
        elif score >= len(self.questions) / 2:
            self.advice_label.text = "You're doing pretty well, but there's room for improvement."
        else:
            self.advice_label.text = "You could use some work. Try to focus on improving your habits."

        # Show the advice label
        self.advice_label.opacity = 1



class MindWave(MDApp):

    def build(self):
        
        # Create the theme and color pallete
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.accent_palette = 'LightBlue'
        
        # Load the file in a variable 
        kv = Builder.load_file ('dashboard2.kv')
        
        # Create Graphs using matplotlib and a JSON file
        
                # Load the data from the JSON file
        try:
            with open("smartwatch_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Get the last date in the data, or set to today if no data exists
        if data:
            last_date = max(data.keys())
            last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()
        else:
            last_date = datetime.date.today() - datetime.timedelta(days=1)

        # Generate random data for the next day and add it to the dictionary
        next_date = last_date + datetime.timedelta(days=1)
        heartrate = random.randint(60, 120)
        steps = random.randint(5000, 15000)
        calories = random.randint(1500, 3000)
        respiratory_rate = random.randint(10, 20)
        data[next_date.strftime("%Y-%m-%d")] = {"heartrate": heartrate, "steps": steps, "calories": calories, "respiratory_rate": respiratory_rate}

        # Save data to JSON file
        with open("smartwatch_data.json", "w") as f:
            json.dump(data, f)

        # Create lists for each metric
        dates = []
        heartrates = []
        steps = []
        calories = []
        respiratory_rates = []

        # Loop through the data and append to the lists
        for date, metrics in data.items():
            dates.append(date)
            heartrates.append(metrics["heartrate"])
            steps.append(metrics["steps"])
            calories.append(metrics["calories"])
            respiratory_rates.append(metrics["respiratory_rate"])

        # Create plots for each metric
        plt.figure(figsize=(10, 8))

        plt.subplot(2, 2, 1)
        plt.plot(dates, heartrates, label="Heartrate", color='steelblue', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Heartrate")
        plt.xticks(rotation=45)
        #plt.gca().set_facecolor('#f0f8ff') Set light blue background

        z = np.polyfit(range(len(dates)), heartrates, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")

        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(dates, steps, label="Steps", color='green', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Steps")
        plt.xticks(rotation=45)

        z = np.polyfit(range(len(dates)), steps, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")

        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(dates, calories, label="Calories", color='orange', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Calories")
        plt.xticks(rotation=45)

        z = np.polyfit(range(len(dates)), calories, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")

        plt.legend()

        plt.subplot(2, 2, 4)
        plt.subplot(2, 2, 4)
        plt.plot(dates, respiratory_rates, label="Respiratory Rate", color='purple', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Respiratory Rate")
        plt.xticks(rotation=45)

        z = np.polyfit(range(len(dates)), respiratory_rates, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")

        plt.legend()

        plt.tight_layout()

        # Display the plot
        kv.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        return kv
        
    



        
MindWave().run()
