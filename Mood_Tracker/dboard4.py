import json
import numpy as np
import datetime
import random
from collections import Counter
from matplotlib import pyplot as plt
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg 
# Η προειδοποίηση (κίτρινα squiggles) δεν επηρεάζει τίποτα.Όλα λειτουργούν όπως πρέπει.


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class QuizWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 5
        # Δημιουργία των ερωτήσεων του κουίζ
        self.questions = [
            "Πώς αισθάνεσαι σήμερα;",
            "Κοιμήθηκες αρκετά χθες το βράδυ;",
            "Έφαγες ένα υγιές γεύμα σήμερα;",
            "Αθλήθηκες σήμερα;"
        ]

        # Δημιουργία των απαντήσεων για κάθε ερώτηση
        self.answers = [
            ["Πολύ καλά", "Καλά", "Μέτρια", "Όχι και τόσο καλά", "Χάλια"],
            ["Ναι", "Όχι"],
            ["Ναι", "Όχι"],
            ["Ναι", "Όχι"]
        ]

        # Δημιουργία ενός dictionary το οποίο περιέχει τις απαντήσεις του χρήστη
        self.user_answers = {}

        # Δημιουργία των quiz labels και answer checkboxes
        self.quiz_labels = []
        self.quiz_checkboxes = []
        for i, question in enumerate(self.questions):
            self.quiz_labels.append(MDLabel(text=question))
            self.quiz_labels[i].font_size = "27"
            self.add_widget(self.quiz_labels[-1])
            for answer in self.answers[i]:
                checkbox = MDCheckbox(group=str(i))
                checkbox.answer = answer
                checkbox.bind(active=self.on_answer)
                self.quiz_checkboxes.append(checkbox)
                self.add_widget(checkbox)
                self.add_widget(MDLabel(text=answer))

            # Δημιουργία μιας γραμμής διαχωρισμού
            separator = MDLabel(text="--------------------------------------------------")
            self.add_widget(separator)

        # Δημιουργία πλήκτρου υποβολής (μη ενεργοποιημένο)
        self.submit_button = MDFillRoundFlatButton(text="Υποβολή", on_press=self.on_submit)
        self.submit_button.disabled = True
        self.add_widget(self.submit_button)

        # Δημιουργία label συμβουλών (κρύμμενο)
        self.advice_label = MDLabel(text="")
        self.add_widget(self.advice_label)
        self.advice_label.opacity = 0
        

    def on_answer(self, checkbox, is_active):
        # Αποθήκευση της απάντησης του χρήστη στο dictionary
        question_index = int(checkbox.group)
        answer = checkbox.answer
        self.user_answers[question_index] = answer

        # Ενεργοποίηση του πλήκτρου υποβολής εφόσον έχουν απαντηθεί οι ερωτήσεις
        if len(self.user_answers) == len(self.questions):
            self.submit_button.disabled = False

    def on_submit(self, button):
        # Calculate the score based on the user's answers
        score = 0
        for answer in self.user_answers.values():
            if answer in  ["Πολύ καλά", "Καλά", "Ναι"]:
                score += 1

        # Create a dictionary to store the user's answers
        result = {
            "answers": self.user_answers
    }

        # Load existing results or initialize an empty list
        try:
            with open("quiz_results.json", "r") as f:
                results = json.load(f)
        except FileNotFoundError:
            results = []

        # Append the new result to the list
        results.append(result)

        # Serialize the list of results to a JSON string
        results_json = json.dumps(results)

        # Write the JSON string to a file
        with open("quiz_results.json", "w") as f:
            f.write(results_json)
        
        # Provide advice based on the score
        advice = ""
        if score == len(self.questions):
            advice = "\n\n\nΤα πηγαίνεις εξαιρετικά! Συνέχισε έτσι! :)"
        elif score >= len(self.questions) / 2:
            advice = "\n\n\nΤα πηγαίνεις πολύ καλά, αλλά υπάρχουν περιθώρια βελτίωσης. :)"
        else:
            advice = "\n\n\nΘα μπορούσες να τα πηγαίνεις και καλύτερα. Προσπαθήστε να επικεντρωθείς στη βελτίωση των συνηθειών σου. :)"

        # Add advice on how to help with insomnia if the user didn't sleep well etc etc
        for question_index, answer in self.user_answers.items():
         if "Κοιμήθηκες αρκετά χθες το βράδυ;" in self.questions[question_index] and answer == "Όχι":
             advice += "\nΕάν αντιμετωπίζετε προβλήματα με τον ύπνο, δοκιμάστε να δημιουργήσετε μια τακτική ρουτίνα ύπνου, να αποφύγετε την καφεΐνη και τα ηλεκτρονικά πριν τον ύπνο και να δημιουργήσετε ένα άνετο περιβάλλον ύπνου."

        for question_index, answer in self.user_answers.items():
         if "Έφαγες ένα υγιές γεύμα σήμερα;" in self.questions[question_index] and answer == "Όχι":
             advice += "\nΕάν δυσκολεύεστε να φάτε, προσπαθήστε να τρώτε μικρότερα, πιο συχνά γεύματα κατά τη διάρκεια της ημέρας και φροντίστε να ενσωματώνετε τροφές που σας αρέσουν και βρίσκετε νόστιμες."

        for question_index, answer in self.user_answers.items():
         if "Αθλήθηκες σήμερα;" in self.questions[question_index] and answer == "Όχι":
             advice += "\nΕάν αντιμετωπίζετε προβλήματα με την άσκηση, προσπαθήστε να βρείτε μια δραστηριότητα που σας αρέσει, ξεκινήστε με μικρούς στόχους και σταδιακά αυξήστε την ένταση και τη διάρκεια και σκεφτείτε να ασκηθείτε με έναν φίλο για κίνητρο."
        
        # Show the advice label
        self.advice_label.text = advice
        self.advice_label.opacity = 1
        self.advice_label.pos = (60,600)
        self.advice_label.font_size = "18"
        

class MindWave(MDApp):

    def build(self):
        
        # Δημιουργία του theme και του colour palette
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'BlueGray'
        
        # load_file του kv design file 
        kv = Builder.load_file ('dashboard2.kv')


        # Ανοιγμα του smartwatch_data.json 
        try:
            with open("smartwatch_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Ευρέση της τελευταίας μέρας που αναγράφεται στα δεδομένα 
        if data:
            last_date = max(data.keys())
            last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()
        else:
            last_date = datetime.date.today() - datetime.timedelta(days=1)

        next_date = last_date + datetime.timedelta(days=1)
        
        # Δημιουργία randomly generated data
        heartrate = random.randint(60, 120)
        steps = random.randint(1000, 15000)
        calories = random.randint(1000, 3000)
        respiratory_rate = random.randint(10, 20)
        hours_slept = random.randint(3, 9)
        body_temperature = random.uniform(35.0, 40.0)
        data[next_date.strftime("%Y-%m-%d")] = {"heartrate": heartrate, "steps": steps, "calories": calories, "respiratory_rate": respiratory_rate, "hours_slept": hours_slept, "body_temperature": body_temperature}

        # Αποθήκευση στο αρχείο JSON
        with open("smartwatch_data.json", "w") as f:
            json.dump(data, f)

        # Δημιουργία lists για κάθε μέτρηση
        dates = []
        heartrates = []
        steps = []
        calories = []
        respiratory_rates = []
        hours_slept = []
        body_temperatures = []
        

        # Loop through the data and append to the lists
        for date, metrics in data.items():
            dates.append(date)
            heartrates.append(metrics["heartrate"])
            steps.append(metrics["steps"])
            calories.append(metrics["calories"])
            respiratory_rates.append(metrics["respiratory_rate"])
            hours_slept.append(metrics["hours_slept"])
            body_temperatures.append(metrics["body_temperature"])
            
        # Δημιουργία γραφημάτων
        plt.figure(figsize=(16, 12))

        plt.subplot(2, 3, 1)
        plt.plot(dates, heartrates, label="Παλμοί", color='steelblue', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Παλμοί")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), heartrates, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.subplot(2, 3, 2)
        plt.plot(dates, steps, label="Βήματα", color='green', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Βήματα")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), steps, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.subplot(2, 3, 3)
        plt.plot(dates, calories, label="Θερμίδες", color='orange', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Θερμίδες")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), calories, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.subplot(2, 3, 4)
        plt.plot(dates, respiratory_rates, label="Ρυθμός Αναπνοών", color='purple', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Ρυθμός Αναπνοών")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), respiratory_rates, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.subplot(2, 3, 5)
        plt.plot(dates, hours_slept, label="Ώρες Ύπνου", color='brown', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Ώρες Ύπνου")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), hours_slept, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.subplot(2, 3, 6)
        plt.plot(dates, body_temperatures, label="Θερμοκρασία Σώματος", color='olive', marker='o', linewidth=2, alpha=0.7)
        plt.grid(axis='y', color='green', linestyle='--', linewidth=0.5)
        plt.ylabel("Θερμοκρασία Σώματος")
        plt.xticks(rotation=45)
        z = np.polyfit(range(len(dates)), body_temperatures, 3)
        p = np.poly1d(z)
        plt.plot(dates, p(range(len(dates))), "b--")
        plt.legend()

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.9)
        plt.subplots_adjust(bottom=0.2)
        

        # Αναπαράσταση των γραφημάτων
        kv.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        with open("quiz_results.json") as f:
            data = json.load(f)

        # Create a dictionary to store the counts for each question
        counts = {i: Counter() for i in range(4)}

        # Loop through the sets of answers and update the counts
        for answers in data:
            for i in range(4):
                answer = answers["answers"].get(str(i))
                if answer:
                    counts[i][answer] += 1

        # Create a 2x2 grid of subplots for the pie charts
        fig, axs = plt.subplots(2, 2)
        
        titles = ["Πώς αισθάνεσαι σήμερα;",
            "Κοιμήθηκες αρκετά χθες το βράδυ;",
            "Έφαγες ένα υγιές γεύμα σήμερα;",
            "Αθλήθηκες σήμερα;"
            ]
        # Loop through each question and create a pie chart
        for i, ax in enumerate(axs.flat):
            ax.set_title(titles[i])
            labels, values = zip(*counts[i].items())
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            
        kv.layout.add_widget(FigureCanvasKivyAgg(plt.gcf()))



        return kv
        
MindWave().run()
