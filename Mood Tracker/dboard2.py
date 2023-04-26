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


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class MindWave(MDApp):

    def build(self):
        
        # Create the theme and color pallete
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.accent_palette = 'LightBlue'
        
        # Load the file in a variable 
        kv = Builder.load_file ('dashboard.kv')
        
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
