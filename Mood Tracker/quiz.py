from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox


class QuizApp(App):
    def build(self):
        # Create the quiz widget
        quiz_widget = QuizWidget()
        return quiz_widget


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
            self.quiz_labels.append(Label(text=question))
            self.add_widget(self.quiz_labels[-1])
            for answer in self.answers[i]:
                checkbox = CheckBox(group=str(i))
                checkbox.answer = answer
                checkbox.bind(active=self.on_answer)
                self.quiz_checkboxes.append(checkbox)
                self.add_widget(checkbox)
                self.add_widget(Label(text=answer))

            # Add a separator between questions
            separator = Label(text="--------------------------------------------------")
            self.add_widget(separator)

        # Create the submit button
        self.submit_button = Button(text="Finish Quiz", on_press=self.on_submit)
        self.submit_button.disabled = True
        self.add_widget(self.submit_button)

        # Create the advice label, but hide it initially
        self.advice_label = Label(text="")
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


if __name__ == "__main__":
    QuizApp().run()


