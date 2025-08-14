import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window


# Initialize the database
def initialize_database():
    conn = sqlite3.connect("pet_care_app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# SignInScreen
class SignInScreen(Screen):
    def __init__(self, **kwargs):
        super(SignInScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        background = Image(source="C:/pet_care_app/back.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        label = Label(text="PAWSITIVE CARE", font_size=40, color=(1, 1, 1, 1),
                      size_hint=(None, None), size=(300, 100), pos_hint={"center_x": 0.5, "center_y": 0.7})
        layout.add_widget(label)

        button_login = Button(text="Login", size_hint=(None, None), size=(200, 50),
                              pos_hint={"center_x": 0.5, "center_y": 0.5}, background_color=(0.2, 0.6, 1, 1))
        button_login.bind(on_press=self.switch_to_login)
        layout.add_widget(button_login)

        button_sign_up = Button(text="Sign Up", size_hint=(None, None), size=(200, 50),
                                pos_hint={"center_x": 0.5, "center_y": 0.3}, background_color=(0.2, 0.6, 1, 1))
        button_sign_up.bind(on_press=self.switch_to_sign_up)
        layout.add_widget(button_sign_up)

        self.add_widget(layout)

    def switch_to_login(self, instance):
        self.manager.current = "login"

    def switch_to_sign_up(self, instance):
        self.manager.current = "sign_up"


import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image

# LoginScreen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        background = Image(source="C:/pet_care_app/back.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        label = Label(text="Login", font_size=30, color=(1, 1, 1, 1), halign="center", size_hint=(None, None),
                      size=(300, 100), pos_hint={"center_x": 0.5, "center_y": 0.9})
        layout.add_widget(label)

        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            multiline=False
        )

        # Bind event to validate input
        self.username_input.bind(text=self.validate_username)
        layout.add_widget(self.username_input)

        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            multiline=False
        )
        layout.add_widget(self.password_input)

        self.error_label = Label(
            text="Invalid credentials",
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )
        self.error_label.opacity = 0
        layout.add_widget(self.error_label)

        button_login = Button(
            text="Login",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0.2, 0.6, 1, 1)
        )
        button_login.bind(on_press=self.login)
        layout.add_widget(button_login)

        button_back = Button(
            text="Back",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            background_color=(0.6, 0.2, 1, 1)
        )
        button_back.bind(on_press=self.switch_back)
        layout.add_widget(button_back)

        self.add_widget(layout)

    def validate_username(self, instance, value):
        # Remove non-alphabetic characters
        filtered_text = ''.join([char for char in value if char.isalpha()])

        # Capitalize the first letter if there's input
        if filtered_text:
            filtered_text = filtered_text[0].upper() + filtered_text[1:]

        # Update the text field
        instance.text = filtered_text

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.error_label.text = "Please fill in all fields"
            self.error_label.opacity = 1
            return

        conn = sqlite3.connect("pet_care_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.error_label.opacity = 0
            self.manager.current = "main"
            self.clear_inputs()
        else:
            self.error_label.text = "Invalid credentials"
            self.error_label.opacity = 1

    def switch_back(self, instance):
        self.manager.current = "signin"
        self.clear_inputs()

    def clear_inputs(self):
        self.username_input.text = ""
        self.password_input.text = ""


import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
import re  # For password validation

# SignUpScreen
class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        background = Image(source="C:/pet_care_app/back.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        label = Label(text="Sign Up", font_size=30, color=(1, 1, 1, 1), halign="center", size_hint=(None, None),
                      size=(300, 100), pos_hint={"center_x": 0.5, "center_y": 0.9})
        layout.add_widget(label)

        # Username Input
        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.75},
            multiline=False
        )

        # Bind event to validate input
        self.username_input.bind(text=self.validate_username)
        layout.add_widget(self.username_input)

        # Password Input
        self.password_input = TextInput(
            hint_text="Password",
            password=True,
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
            multiline=False
        )

        # Bind event to validate password
        self.password_input.bind(text=self.validate_password)
        layout.add_widget(self.password_input)

        # Confirm Password Input
        self.confirm_password_input = TextInput(
            hint_text="Confirm Password",
            password=True,
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            multiline=False
        )
        layout.add_widget(self.confirm_password_input)

        # Error Label
        self.error_label = Label(
            text="",
            color=(1, 0, 0, 1),
            size_hint=(None, None),
            size=(250, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.45}
        )
        self.error_label.opacity = 0
        layout.add_widget(self.error_label)

        # Sign Up Button
        button_signup = Button(
            text="Sign Up",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            background_color=(0.2, 0.6, 1, 1)
        )
        button_signup.bind(on_press=self.sign_up)
        layout.add_widget(button_signup)

        # Back Button
        button_back = Button(
            text="Back",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            background_color=(0.6, 0.2, 1, 1)
        )
        button_back.bind(on_press=self.switch_back)
        layout.add_widget(button_back)

        self.add_widget(layout)

    def validate_username(self, instance, value):
        """Ensure username contains only letters & auto-capitalize the first letter."""
        filtered_text = ''.join([char for char in value if char.isalpha()])
        
        if filtered_text:
            filtered_text = filtered_text[0].upper() + filtered_text[1:]

        instance.text = filtered_text

    def validate_password(self, instance, value):
        """Ensure password is at least 5 characters, starts with a letter, and has at least one number & special character."""
        if len(value) < 5:
            self.error_label.text = "Password must be at least 5 characters long"
            self.error_label.opacity = 1
            return

        if not re.match(r"^[A-Za-z]", value):
            self.error_label.text = "Password must start with a letter"
            self.error_label.opacity = 1
            return

        if not re.search(r"\d", value):
            self.error_label.text = "Password must contain at least one number"
            self.error_label.opacity = 1
            return

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            self.error_label.text = "Password must contain at least one special character"
            self.error_label.opacity = 1
            return

        self.error_label.opacity = 0  # Hide error if password is valid

    def sign_up(self, instance):
        """Handle sign-up validation and database storage."""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not username or not password or not confirm_password:
            self.error_label.text = "Please fill in all fields"
            self.error_label.opacity = 1
            return

        if password != confirm_password:
            self.error_label.text = "Passwords do not match"
            self.error_label.opacity = 1
            return

        # Check password validity again before saving
        if len(password) < 5 or not re.match(r"^[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            self.error_label.text = "Invalid password format"
            self.error_label.opacity = 1
            return

        # Database Connection
        conn = sqlite3.connect("pet_care_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            self.error_label.text = "Username already taken"
            self.error_label.opacity = 1
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()

            self.error_label.opacity = 0
            self.manager.current = "signin"
            self.clear_inputs()

    def switch_back(self, instance):
        """Switch to the sign-in screen."""
        self.manager.current = "signin"
        self.clear_inputs()

    def clear_inputs(self):
        """Clear all input fields."""
        self.username_input.text = ""
        self.password_input.text = ""
        self.confirm_password_input.text = ""





import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty


# Function to initialize the database
def initialize_database():
    """
    Creates the 'pets_info_details' table in the database if it doesn't exist.
    """
    try:
        connection = sqlite3.connect("pet_care_app.db")  # Ensure correct path to the database
        cursor = connection.cursor()

        # Create the 'pets_info_details' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets_info_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_type TEXT,
                gender TEXT,
                breed TEXT,
                weight REAL,
                age INTEGER,
                longevity REAL,
                grooming_frequency TEXT,
                lifetime_cost REAL,
                food_cost REAL,
                breed_name TEXT
            )
        """)

        connection.commit()
        print("Database tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database tables: {e}")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if connection:
            connection.close()

# Call the function to initialize the database at the start
initialize_database()


# Sample prediction functions (you would need to replace these with actual models)
def predict_longevity(animal_type, breed_encoded, age, gender, weight):
    return 10  # Placeholder value

def predict_grooming_frequency(animal_type, breed_encoded, age, gender, weight):
    return "Weekly"  # Placeholder value

def predict_lifetime_cost(animal_type, breed_encoded, age, gender, weight):
    return 1000  # Placeholder value

def predict_food_cost(animal_type, breed_encoded, age, gender, weight):
    return 200  # Placeholder value


# Function to encode breed (replace with your actual encoding logic)
def encode_breed(breed):
    return 1  # Placeholder for encoding (should return -1 if invalid)



import re
import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import StringProperty


class PetInfoScreen(Screen):
    def __init__(self, **kwargs):
        super(PetInfoScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        # Set the background image
        background = Image(source="C:/pet_care_app/pet.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Title: Pet Info
        title_label = Label(text="Pet Info", color=(1, 1, 1, 1), font_size=60, bold=True, size_hint=(None, None),
                            size=(Window.width * 0.8, 50), pos_hint={"center_x": 0.5, "top": 0.95})
        layout.add_widget(title_label)

        # Error Label for validation messages
        self.error_label = Label(text="", color=(1, 0, 0, 1), font_size=24, size_hint=(None, None),
                                 pos_hint={"center_x": 0.5, "top": 0.85})
        self.error_label.opacity = 0  # Hide by default
        layout.add_widget(self.error_label)

        # Create a form for pet details
        form_layout = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(Window.width * 0.8, Window.height * 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )

        # Animal Type field with ToggleButton
        animal_type_layout = BoxLayout(orientation="horizontal", size_hint=(None, None),
                                       size=(Window.width * 0.8, 50), padding=[0, 40, 0, 20])
        animal_type_label = Label(text="Animal Type (Dog/Cat):", color=(1, 1, 1, 1), font_size=32, bold=True)

        # Toggle buttons for animal type
        self.dog_button = ToggleButton(text="Dog", size_hint=(None, None), size=(100, 40), group="animal_type")
        self.cat_button = ToggleButton(text="Cat", size_hint=(None, None), size=(100, 40), group="animal_type")

        # Set default selection
        self.dog_button.state = "down"

        # Add widgets to layout
        animal_type_layout.add_widget(animal_type_label)
        animal_type_layout.add_widget(self.dog_button)
        animal_type_layout.add_widget(self.cat_button)
        form_layout.add_widget(animal_type_layout)

        # Gender field - Only letters, auto-capitalize first letter
        self.gender_input = TextInput(
            hint_text="Enter Male or Female",
            size_hint=(None, None),
            size=(400, 40),
            multiline=False
        )
        self.gender_input.bind(text=self.validate_text)
        form_layout.add_widget(Label(text="Gender:", color=(1, 1, 1, 1), font_size=32, bold=True))
        form_layout.add_widget(self.gender_input)

        # Breed field - Only letters, auto-capitalize first letter
        self.breed_input = TextInput(
            hint_text="Enter Breed",
            size_hint=(None, None),
            size=(400, 40),
            multiline=False
        )
        self.breed_input.bind(text=self.validate_text)
        form_layout.add_widget(Label(text="Breed:", color=(1, 1, 1, 1), font_size=32, bold=True))
        form_layout.add_widget(self.breed_input)

        # Age field - Only numbers (max 2 digits)
        self.age_input = TextInput(
            hint_text="Enter Age",
            size_hint=(None, None),
            size=(400, 40),
            multiline=False
        )
        self.age_input.bind(text=self.validate_numeric)
        form_layout.add_widget(Label(text="Age:", color=(1, 1, 1, 1), font_size=32, bold=True))
        form_layout.add_widget(self.age_input)

        # Weight field - Only numbers (max 2 digits)
        self.weight_input = TextInput(
            hint_text="Enter Weight in kg",
            size_hint=(None, None),
            size=(400, 40),
            multiline=False
        )
        self.weight_input.bind(text=self.validate_numeric)
        form_layout.add_widget(Label(text="Weight (kg):", color=(1, 1, 1, 1), font_size=32, bold=True))
        form_layout.add_widget(self.weight_input)

        # Submit button
        submit_button = Button(text="Submit", size_hint=(None, None), size=(200, 50),
                               background_color=(0.2, 0.6, 1, 1), pos_hint={"center_x": 0.5, "top": 0.4})
        submit_button.bind(on_press=self.submit_form)
        layout.add_widget(submit_button)

        # Add form layout
        layout.add_widget(form_layout)
        self.add_widget(layout)

    # Validation function for Gender and Breed (Only letters, auto-capitalize first letter)
    def validate_text(self, instance, value):
        filtered_text = ''.join([char for char in value if char.isalpha() or char == ' '])
        if filtered_text:
            filtered_text = filtered_text[0].upper() + filtered_text[1:]  # Capitalize first letter
        instance.text = filtered_text

    # Validation function for Age and Weight (Only numbers, max 2 digits)
    def validate_numeric(self, instance, value):
        filtered_text = ''.join([char for char in value if char.isdigit()])[:2]  # Restrict to 2 digits
        instance.text = filtered_text

    def submit_form(self, instance):
        # Retrieve inputs from the form
        animal_type = "Dog" if self.dog_button.state == "down" else "Cat"
        gender = self.gender_input.text.strip()
        breed = self.breed_input.text.strip()
        age = self.age_input.text.strip()
        weight = self.weight_input.text.strip()

        # Validation
        if not gender or not breed or not age or not weight:
            self.error_label.text = "All fields are required!"
            self.error_label.opacity = 1
            return

        if len(age) > 2 or len(weight) > 2:
            self.error_label.text = "Age and Weight must be max 2 digits!"
            self.error_label.opacity = 1
            return

        # If all validations pass, hide the error label
        self.error_label.opacity = 0

        print("Valid inputs! Saving to database...")
        self.save_pet_info(animal_type, gender, breed, int(age), int(weight))

    

    


   

    def go_back(self):
        self.manager.current = "main"

    def go_to_diseases(self):
        self.manager.current = "diseases"





from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import os  # For handling file paths

class DiseasesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Background Image (Using relative path)
        image_path = os.path.join(os.getcwd(), "diseases1.jpeg")  # Ensure the image is in the same directory
        if os.path.exists(image_path):  # Check if image exists
            background_image = Image(source=image_path, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
            layout.add_widget(background_image)
        else:
            print("Warning: Background image not found!")

        # Scrollable Form
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_content = BoxLayout(orientation='vertical', size_hint_y=None, padding=20, spacing=10)
        scroll_content.bind(minimum_height=scroll_content.setter('height'))

        # Title
        title_label = Label(text="Disease Prediction Form", color=(1, 1, 1, 1), font_size=40, bold=True,
                            pos_hint={'center_x': 0.5, 'top': 0.93})
        scroll_content.add_widget(title_label)

        # Animal Type Field
        animal_type_layout = self.create_toggle_buttons("Animal Type:", ["Dog", "Cat"], "animal_type")
        self.dog_button, self.cat_button = animal_type_layout[1]
        scroll_content.add_widget(animal_type_layout[0])

        # Breed Input
        self.breed_input = self.create_text_input("Breed:", "Enter breed")
        scroll_content.add_widget(self.breed_input)

        # Gender Selection
        gender_layout = self.create_toggle_buttons("Gender:", ["Male", "Female"], "gender")
        self.male_button, self.female_button = gender_layout[1]
        scroll_content.add_widget(gender_layout[0])

        # Age Input
        self.age_input = self.create_text_input("Age (in years):", "Enter age")
        scroll_content.add_widget(self.age_input)

        # Weight Input
        self.weight_input = self.create_text_input("Weight (kg):", "Enter weight")
        scroll_content.add_widget(self.weight_input)

        # Body Temperature Input
        self.body_temperature_input = self.create_text_input("Body Temperature (°C):", "Enter temperature")
        scroll_content.add_widget(self.body_temperature_input)

        # Heart Rate Input (Newly Added)
        self.heart_rate_input = self.create_text_input("Heart Rate (bpm):", "Enter heart rate")
        scroll_content.add_widget(self.heart_rate_input)

        # Disease-Related Questions
        disease_questions = [
            "Is the pet showing appetite loss?",
            "Is the pet vomiting?",
            "Is the pet having diarrhea?",
            "Is the pet coughing?",
            "Is the pet having labored breathing?",
            "Is the pet showing lameness?",
            "Is the pet having skin lesions?",
            "Is the pet having nasal discharge?",
            "Is the pet having eye discharge?"
        ]

        self.disease_toggles = {}  # Store references to toggle buttons

        for idx, question in enumerate(disease_questions):
            layout, toggles = self.create_toggle_buttons(question, ["Yes", "No"], f"disease_{idx}")
            self.disease_toggles[question] = toggles[0]  # Store the "Yes" button reference
            scroll_content.add_widget(layout)

        # Submit and Back Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width * 0.8, 100),
                                  pos_hint={'center_x': 0.5})

        submit_button = Button(text="Submit", size_hint=(None, None), size=(200, 50), background_color=(0.2, 0.6, 1, 1))
        submit_button.bind(on_press=self.submit_form)
        button_layout.add_widget(submit_button)

        back_button = Button(text="Back", size_hint=(None, None), size=(100, 50), background_color=(0.8, 0.2, 0.2, 1))
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)

        scroll_content.add_widget(button_layout)

        scroll_view.add_widget(scroll_content)
        layout.add_widget(scroll_view)
        self.add_widget(layout)
    
    

    def create_text_input(self, label_text, hint_text):
        """ Helper function to create labeled text inputs. """
        layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width * 0.8, 50),
                           pos_hint={'center_x': 0.5})
        label = Label(text=label_text, color=(1, 1, 1, 1), font_size=24)
        layout.add_widget(label)
        text_input = TextInput(hint_text=hint_text, size_hint=(None, None), size=(200, 40))
        layout.add_widget(text_input)
        return text_input

    def create_toggle_buttons(self, label_text, options, group):
        """ Helper function to create labeled toggle buttons. """
        layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(Window.width * 0.8, 50),
                           pos_hint={'center_x': 0.5})
        label = Label(text=label_text, color=(1, 1, 1, 1), font_size=24)
        layout.add_widget(label)

        buttons = []
        for i, option in enumerate(options):
            button = ToggleButton(text=option, size_hint=(None, None), size=(100, 40), group=group)
            if i == 0:
                button.state = "down"  # Default selection
            buttons.append(button)
            layout.add_widget(button)

        return layout, buttons

    def submit_form(self, instance):
        """ Collects form data and predicts diseases. """
        try:
            animal_type = "Dog" if self.dog_button.state == 'down' else "Cat"
            breed = self.breed_input.text.strip()
            gender = "Male" if self.male_button.state == 'down' else "Female"
            age = int(self.age_input.text.strip())
            weight = float(self.weight_input.text.strip())
            body_temperature = float(self.body_temperature_input.text.strip())
            heart_rate = int(self.heart_rate_input.text.strip())  # Newly Added

            # Collect disease-related answers
            disease_data = {q: int(self.disease_toggles[q].state == 'down') for q in self.disease_toggles}

            # Call predict_diseases function
            disease = predict_diseases(animal_type, breed, gender, age, weight, body_temperature, heart_rate, disease_data)

            print(f"Predicted Disease: {disease}")  # Debugging output

        except ValueError:
            print("Error: Invalid input detected. Please ensure all fields are correctly filled.")

    def go_back(self, instance):
        """ Navigates back to the pet information screen. """
        self.manager.current = "pet_info"

    def go_to_chatbot(self, instance):
        """ Navigates to the chatbot screen. """
        self.manager.current = "chatbot_screen"






from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class ChatbotScreen(Screen):
    def on_kv_post(self, base_widget):
        """ Assigns widget references after KV file is loaded """
        self.chat_area = self.ids.get("chat_area", None)
        self.user_input = self.ids.get("user_input", None)
        
        if not self.chat_area or not self.user_input:
            print("Error: Ensure 'chat_area' and 'user_input' are defined in the KV file.")

    def send_message(self):
        if not self.user_input:
            print("Error: user_input is None. Ensure it is defined in the KV file.")
            return

        user_message = self.user_input.text.strip()
        if user_message:
            self.add_message(f"[color=0000FF]User:[/color] {user_message}")
            bot_response = self.chatbot_response(user_message)
            self.add_message(f"[color=008000]Chatbot:[/color] {bot_response}")
            self.user_input.text = ""

    def add_message(self, message):
        label = Label(
            text=message,
            markup=True,
            size_hint_y=None,
            height=40,
            text_size=(self.chat_area.width - 20, None),
            halign="left",
            valign="top",
        )
        self.chat_area.add_widget(label)
        self.chat_area.height = self.chat_area.minimum_height
        self.chat_area.parent.scroll_y = 1  # Scroll to bottom

    def chatbot_response(self, message):
        responses = {
            "hello": "Hello! How can I help you today?",
            "bye": "Goodbye! Have a great day!",
            "how are you": "I'm doing great, thank you for asking!",
            "thanks": "You're welcome! Let me know if you need anything.",
            "help": "I'm here to assist you. How can I help?",
            "canine parvovirus": "Canine Parvovirus (CPV) is caused by the virus spreading through direct contact with infected dogs, especially their feces, saliva, or vomit. It can also spread through contaminated environments or objects, as the virus survives for a long time outside the host.",
            "feline panleukopenia": "Feline Panleukopenia, also known as feline distemper, is caused by the feline parvovirus, which spreads through direct contact with infected animals or contaminated surfaces.",
            "parvovirus": "Parvovirus in pets is a viral infection that affects dogs and cats, causing severe gastrointestinal issues, and spreads through contact with infected feces or contaminated objects.",
            "feline calicivirus": "Feline Calicivirus is a viral infection that affects cats, causing respiratory symptoms and oral ulcers. It spreads through direct contact with infected cats or contaminated objects.",
            "canine flu": "Canine Flu is caused by the H3N8 or H3N2 influenza virus, which spreads through respiratory droplets, often in crowded places like kennels or dog parks.",
            "pancreatitis": "Pancreatitis is inflammation of the pancreas, often caused by high-fat diets, obesity, infections, or certain medications.",
            "gastroenteritis": "Gastroenteritis in pets is typically caused by infections from viruses (such as Parvovirus or Canine Coronavirus), bacteria (like Salmonella or E. coli), or parasites, often spread through contaminated food or water.",
            "feline herpesvirus": "Feline Herpesvirus is a viral infection that causes respiratory issues in cats. It spreads through direct contact with an infected cat's nasal secretions or saliva.",
            "hyperthyroidism": "Hyperthyroidism in cats is caused by overproduction of thyroid hormones, often due to benign tumors of the thyroid gland.",
            "canine hepatitis": "Canine Hepatitis is caused by the Canine Adenovirus-1 (CAV-1) virus, transmitted through contact with infected urine, saliva, or feces.",
            "upper respiratory infection": "Upper Respiratory Infection in pets is commonly caused by viral infections (such as Canine Adenovirus, Distemper Virus, or Parainfluenza) and bacterial infections (such as Bordetella bronchiseptica), often spread through airborne droplets from infected pets.",
            "feline upper respiratory infection": "Feline Upper Respiratory Infections are commonly caused by viruses such as feline herpesvirus and calicivirus, spread through nasal secretions, saliva, or contaminated surfaces.",
            "feline viral rhinotracheitis": "Feline Viral Rhinotracheitis is caused by feline herpesvirus, leading to respiratory issues, spread through contact with infected cats or their secretions.",
            "canine distemper": "Canine Distemper is caused by a virus (Canine Distemper Virus), which is spread through direct contact with an infected dog or through airborne droplets from coughing and sneezing.",
            "feline respiratory disease complex": "Feline Respiratory Disease Complex is caused by a combination of viral (feline herpesvirus, calicivirus) and bacterial infections (e.g., *Bordetella*), leading to respiratory distress.",
            "feline rhinotracheitis": "Feline Rhinotracheitis is caused by feline herpesvirus, which causes inflammation in the respiratory tract of cats, spreading through nasal secretions or saliva.",
            "kennel cough": "Kennel Cough is caused by a combination of viral and bacterial infections, including Bordetella bronchiseptica and Canine Parainfluenza Virus, often transmitted in crowded environments like kennels.",
            "feline infectious peritonitis": "Feline Infectious Peritonitis (FIP) is caused by a mutated form of the feline coronavirus, typically spread through direct contact with infected feces or bodily fluids.",
            "feline chlamydia": "Feline Chlamydia is caused by *Chlamydia felis*, a bacterium that infects the eyes and respiratory system of cats, spread through direct contact with infected animals or their secretions.",
            "canine leptospirosis": "Canine Leptospirosis is caused by bacteria from the genus *Leptospira*, which are transmitted through contact with contaminated water, soil, or urine from infected animals.",
            "feline leukemia virus": "Feline Leukemia Virus (FeLV) is caused by a retrovirus that is spread through saliva, urine, feces, or bites from an infected cat.",
            "leptospirosis": "Leptospirosis is a bacterial infection caused by *Leptospira* species, which are transmitted through contact with contaminated water, soil, or urine from infected animals.",
            "canine influenza": "Canine Influenza is caused by the H3N8 or H3N2 influenza virus, which spreads through respiratory droplets, particularly in crowded environments.",
            "feline panleukopenia virus": "Feline Panleukopenia is caused by the feline parvovirus, transmitted through direct contact with infected animals or contaminated surfaces.",
            "canine hepatitis": "Canine Hepatitis is caused by Canine Adenovirus-1 (CAV-1), which is transmitted through infected urine, saliva, or feces.",
            "feline asthma": "Feline Asthma is often triggered by allergens, respiratory infections, or environmental factors like dust, smoke, and pollen.",
            "feline upper respiratory infection": "Feline Upper Respiratory Infection is caused by viruses like feline herpesvirus and calicivirus, spread through nasal secretions or saliva.",
            "canine heartworm disease": "Canine Heartworm Disease is caused by *Dirofilaria immitis* worms, transmitted by mosquito bites that deposit infective larvae into the dog's bloodstream.",
            "feline infectious peritonitis": "Feline Infectious Peritonitis (FIP) is caused by a mutated form of the feline coronavirus, spread through bodily fluids or infected feces.",
            "feline calicivirus": "Feline Calicivirus is a viral infection that affects cats, often causing respiratory issues and oral ulcers. Spread through saliva, nasal secretions, or contaminated surfaces.",
        }

        message_lower = message.lower()
        found_responses = [responses[key] for key in responses if key in message_lower]
        return " ".join(found_responses) if found_responses else "I'm sorry, I didn't understand that."

    def go_back(self):
        self.manager.current = "pet_info"


class PetInfoScreen(Screen):
    pass  # Placeholder

class DiseasesScreen(Screen):
    pass  # Placeholder

class PetCareApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PetInfoScreen(name="pet_info"))
        sm.add_widget(DiseasesScreen(name="diseases"))
        sm.add_widget(ChatbotScreen(name="chatbot"))
        return sm

if __name__ == "__main__":
    PetCareApp().run()





















import sqlite3
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.core.window import Window
import joblib
import pandas as pd

# Dog and Cat Breeds
dog_breeds = {1: "Akita", 2: "Beagle", 3: "Border Collie", 4: "Boxer", 5: "Bulldog", 6: "Chihuahua",
              7: "Cocker Spaniel", 8: "Corgi", 9: "Dachshund", 10: "Dalmatian", 11: "Doberman Pinscher",
              12: "German Shepherd", 13: "Golden Retriever", 14: "Husky", 15: "Labrador",
              16: "Labrador Retriever", 17: "Pit Bull", 18: "Poodle", 19: "Rottweiler",
              20: "Shih Tzu", 21: "Siberian Husky", 22: "Yorkshire Terrier"}

cat_breeds = {23: "Abyssinian", 24: "American Curl", 25: "Bengal", 26: "Bombay", 27: "British Shorthair",
              28: "Burmese", 29: "Devon Rex", 30: "Maine Coon", 31: "Manx", 32: "Persian",
              33: "Ragdoll", 34: "Russian Blue", 35: "Scottish Fold", 36: "Siamese",
              37: "Siberian", 38: "Sphynx"}



class FindYourPetMatchScreen(Screen):
    def __init__(self, **kwargs):
        super(FindYourPetMatchScreen, self).__init__(**kwargs)

        # Load the trained model
        self.adoption = joblib.load("C:\\pet_care_app\\models\\adoption.pkl")

        layout = FloatLayout()

        # Background Image
        background = Image(source="C:/pet_care_app/petmatch.jpeg", allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Title
        title_label = Label(
            text="Find Your Pet Match", color=(1, 1, 1, 1), font_size=60, bold=True,
            size_hint=(None, None), size=(Window.width * 0.8, 50),
            pos_hint={"center_x": 0.6, "top": 0.95}
        )
        layout.add_widget(title_label)

        # Form Layout
        form_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(Window.width * 0.8, Window.height * 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )

        # Animal Type
        animal_type_layout = BoxLayout(orientation='horizontal')
        animal_type_label = Label(text="Animal Type (Dog/Cat):", color=(1, 1, 1, 1), font_size=32, bold=True)
        self.dog_button = ToggleButton(text="Dog", size_hint=(None, None), size=(100, 40), group="animal_type", state="down")
        self.cat_button = ToggleButton(text="Cat", size_hint=(None, None), size=(100, 40), group="animal_type")
        animal_type_layout.add_widget(animal_type_label)
        animal_type_layout.add_widget(self.dog_button)
        animal_type_layout.add_widget(self.cat_button)
        form_layout.add_widget(animal_type_layout)

        # Height
        height_layout = BoxLayout(orientation='horizontal')
        height_label = Label(text="Height (inches):", color=(1, 1, 1, 1), font_size=32, bold=True)
        self.height_input = TextInput(hint_text="Enter pet height", input_filter='float', size_hint=(None, None), size=(200, 40))
        height_layout.add_widget(height_label)
        height_layout.add_widget(self.height_input)
        form_layout.add_widget(height_layout)

        # Space Requirement
        space_requirement_layout = BoxLayout(orientation='horizontal')
        space_requirement_label = Label(text="Space Requirement:", color=(1, 1, 1, 1), font_size=32, bold=True)
        self.space_requirement_dropdown = Spinner(
            text="Select Size",
            values=["Small(100-250sqt)", "Medium(250-400sqt)", "Large(400-600sqt)"],
            size_hint=(None, None),
            size=(200, 40)
        )
        space_requirement_layout.add_widget(space_requirement_label)
        space_requirement_layout.add_widget(self.space_requirement_dropdown)
        form_layout.add_widget(space_requirement_layout)

        # Stay In
        stay_in_layout = BoxLayout(orientation='horizontal')
        stay_in_label = Label(text="Stay In:", color=(1, 1, 1, 1), font_size=32, bold=True)
        self.stay_in_dropdown = Spinner(
            text="Select Stay Type",
            values=["Indoor", "Outdoor", "Both"],
            size_hint=(None, None),
            size=(200, 40)
        )
        stay_in_layout.add_widget(stay_in_label)
        stay_in_layout.add_widget(self.stay_in_dropdown)
        form_layout.add_widget(stay_in_layout)

        # Predicted Breed Label
        self.predicted_breed_label = Label(
            text="Predicted Breed: Not yet predicted",
            color=(1, 1, 1, 1),
            font_size=32
        )
        form_layout.add_widget(self.predicted_breed_label)

        # Submit Button
        submit_button = Button(
            text="Submit",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.2, 0.6, 1, 1),
            pos_hint={"center_x": 0.5}
        )
        submit_button.bind(on_press=self.submit_form)
        form_layout.add_widget(submit_button)

        layout.add_widget(form_layout)
        self.add_widget(layout)

        # Back Button
        back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(150, 50),
            background_color=(1, 0, 0, 1),  # Red color for visibility
            pos_hint={"center_x": 0.5, "y": 0.05}  # Adjust position
            )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)  # Add to the layout


    def submit_form(self, instance):
        try:
            animal_type = 1 if self.dog_button.state == 'down' else 0
            height = float(self.height_input.text.strip()) if self.height_input.text.strip() else 0
            space_mapping = {"Small(100-250sqt)": 100, "Medium(250-400sqt)": 250, "Large(400-600sqt)": 400}
            space_requirement = space_mapping.get(self.space_requirement_dropdown.text, 200)
            stay_mapping = {"Indoor": 0, "Outdoor": 1, "Both": 2}
            stay_in = stay_mapping.get(self.stay_in_dropdown.text, 1)

            features_df = pd.DataFrame({'stay': [stay_in], 'Space requirement': [space_requirement], 'height(inches)': [height], 'Animal_Type': [animal_type]})
            predicted_index = int(self.adoption.predict(features_df)[0])
            breed_list = dog_breeds if animal_type == 1 else cat_breeds
            predicted_breed = breed_list.get(predicted_index, next(iter(breed_list.values())))

            conn = sqlite3.connect("pet_care_app.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pet_adoptions (stay, space_requirement, height, animal_type, predicted_breed) VALUES (?, ?, ?, ?, ?)", (stay_in, space_requirement, height, animal_type, predicted_breed))
            conn.commit()
            conn.close()

            self.predicted_breed_label.text = f"Predicted Breed: {predicted_breed}"
        except Exception as e:
            self.predicted_breed_label.text = f"Error: {e}"


    def go_back(self, instance):
        """ Navigate back to the main screen. """
        self.manager.current = "main"














    









from kivy.uix.image import Image
from kivy.core.window import Window

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Create main layout
        layout = FloatLayout()

        # Set background color to #078E70
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(7 / 255, 142 / 255, 112 / 255, 1)  # Color #078E70
            self.rect = Rectangle(size=self.size, pos=self.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

         # Title label: "Pet Care Assistant"
        title_label = Label(
            text="PAWSITIVE CARE",
            font_size=60,  # Bigger size for the heading
            bold=True,
            color=(1, 1, 1, 1),  # White color
            size_hint=(None, None),
            size=(Window.width * 0.8, 60),  # Adjusted size
            pos_hint={"center_x": 0.5, "top": 0.98}
        )
        layout.add_widget(title_label)

        subheading_label = Label(
    text="Basic Tips",
    font_size=52,  # Slightly bigger size for the subheading
    bold=True,  # Bold text
    color=(0, 0, 0, 1),  # Black color
    size_hint=(None, None),
    size=(Window.width * 0.8, 50),  # Adjusted size for the subheading
    pos_hint={"x": 0.05, "top": 0.88},  # Positioned near the left edge (x: 0.05)
    halign="left",  # Align text to the left
)
        layout.add_widget(subheading_label)

        # Buttons layout (horizontal, placed next to each other at the right side of the screen)
        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(Window.width * 0.3, 50),
            pos_hint={"right": 0.85, "top": 0.9},  # Positioned a little more to the left (right: 0.95)
            spacing=10  # Space between buttons
        )

        button_add_pets_info = Button(
            text="Add pets details",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.2, 0.6, 1, 1)
        )
        button_add_pets_info.bind(on_press=self.change_screen)
       

        button_find_your_pet_match = Button(
            text="Find your pet match",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.2, 0.6, 1, 1)
        )
        button_find_your_pet_match.bind(on_press=self.change_screen)

        

        button_logout = Button(
            text="Logout",
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.2, 0.6, 1, 1)
        )

        # Add buttons to the button layout
        button_layout.add_widget(button_add_pets_info)
        button_layout.add_widget(button_find_your_pet_match)
        button_layout.add_widget(button_logout)

        # Add the button layout to the main layout
        layout.add_widget(button_layout)

        # Background image (mainpic.jpeg) positioned below the buttons with 80% height and 40% width
        background = Image(source="C:/pet_care_app/mainpic.png", allow_stretch=True, keep_ratio=False,
                           size_hint=(None, None), size=(Window.width * 0.4, Window.height * 0.8),
                           pos_hint={"right": 1, "top": 0.75})  # Slightly move the image above (top: 0.48)
        layout.add_widget(background)

        # Scrollable task list (inside ScrollView) with increased height
        scroll_view = ScrollView(
            size_hint=(1, None),
            height=800,  # Increased height of the scroll view
            pos_hint={"top": 0.8}
        )

        task_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.8, None),  # Set the width to 80%
            spacing=10,
            padding=[20, 20]
        )
        task_layout.bind(minimum_height=task_layout.setter('height'))

        # Detailed daily care tasks
        tasks = [
            ("1. Clean the Pet’s Living Area", "Ensure that your pet's living space is clean and comfortable. For dogs, this means washing bedding, wiping down play areas, and ensuring cleanliness in crates. For cats, scoop the litter box daily and replace litter as needed."),
            ("2. Provide Fresh Water", "Always make sure your pet has access to clean, fresh water. Regularly check water bowls and refill them throughout the day to keep your pet hydrated."),
            ("3. Feeding", "Stick to a consistent feeding schedule, offering food appropriate to your pet's age, size, and health needs. Typically, pets should be fed twice a day, but follow recommendations from your veterinarian."),
            ("4. Daily Walks for Dogs", "Dogs need daily exercise, so take them for a walk at least once a day. Walks provide both physical exercise and mental stimulation."),
            ("5. Use of Leash or Collar", "When going outside, ensure your dog wears a collar with ID tags and is securely fastened with a leash. For cats, if they are leash trained, use a harness during outdoor excursions."),
            ("6. Check for Health Issues", "Regularly check your pet’s fur, skin, ears, and nails to catch any early signs of health problems. Look for signs of parasites like fleas or ticks and address them immediately.")
        ]

        # Adding each task and description to the task layout
        for task, description in tasks:
            task_label = Label(
                text=f"[b]{task}[/b]",
                font_size=42,
                size_hint=(1, None),
                height=60,
                halign="left",
                valign="top",
                color=(1, 1, 1, 1),  # White color
                markup=True
            )
            task_label.bind(size=task_label.setter('text_size'))  # Enable text wrapping

            description_label = Label(
                text=description,
                font_size=28,
                size_hint=(1, None),
                height=80,
                halign="left",
                valign="top",
                color=(1, 1, 1, 1)  # White color
            )
            description_label.bind(size=description_label.setter('text_size'))  # Enable text wrapping

            # Add task labels to the task layout
            task_layout.add_widget(task_label)
            task_layout.add_widget(description_label)

        # Add the task layout to the scroll view
        scroll_view.add_widget(task_layout)

        # Add the scroll view to the main layout
        layout.add_widget(scroll_view)

        # Add the layout to the screen
        self.add_widget(layout)

        button_logout.bind(on_press=self.logout)

    def _update_rect(self, *args):
        # Update the background rectangle size when layout is resized
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_screen(self, instance):
        # Ensure the button text matches exactly
        if instance.text == "Find your pet match":
            self.manager.current = "pet_match"
        elif instance.text == "Add pets details":  # Corrected comparison here
            self.manager.current = "pet_info" 

    def logout(self, instance):
        # Define logout behavior here
        print("Logging out...")
        self.manager.current = "signin"



class PetCareApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignInScreen(name="signin"))  # Add SignInScreen first
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="sign_up"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(PetInfoScreen(name="pet_info")) 
        sm.add_widget(FindYourPetMatchScreen(name="pet_match"))
        sm.add_widget(ChatbotScreen(name="chatbot"))
        
        sm.current = "signin"  # Set the initial screen to signin
        return sm



if __name__ == "__main__":
    PetCareApp().run()