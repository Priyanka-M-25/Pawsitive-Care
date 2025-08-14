import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
from main import HomeScreen
from signin import MainScreen, PetInfoScreen, FindYourPetMatchScreen, SignInScreen, LoginScreen, SignUpScreen, DiseasesScreen, ChatbotScreen

# Load the UI definition from signin.kv
Builder.load_file("signin.kv")

# Initialize the LabelEncoder globally
label_encoder = LabelEncoder()

# Load and fit the LabelEncoder with breed data
data = pd.read_csv('C:\\pet_care_app\\dogcatdb.csv')  # Update with your actual data path
label_encoder.fit(data['Breed'])  # Fit the encoder on the 'Breed' column

# Load the trained models (update paths as necessary)
longevity_model = joblib.load('C:\\pet_care_app\\models\\longevity1_model.pkl')
grooming_model = joblib.load('C:\\pet_care_app\\models\\grooming_model.pkl')
lifetime_cost_model = joblib.load('C:\\pet_care_app\\models\\lifetime_cost_predictor_model.pkl')
food_cost_model = joblib.load('C:\\pet_care_app\\models\\food_cost_prediction_model.pkl')
disease_model = joblib.load('C:\\pet_care_app\\models\\disease_prediction_model.pkl')
adoption = joblib.load('C:\\pet_care_app\\models\\adoption.pkl')


# Function to encode a breed
def encode_breed(breed):
    breed_lower = breed.lower()
    found_breed = next((class_name for class_name in label_encoder.classes_
                        if class_name.lower() == breed_lower), None)
    if found_breed:
        return label_encoder.transform([found_breed])[0]
    return -1  # Return -1 if breed not found

# Prediction functions using the trained models
def predict_longevity(animal_type, breed_encoded, age, gender, weight):
    animal_type_numeric = 1 if animal_type.lower() == 'dog' else 0  # 1 for dog, 0 for cat
    gender_numeric = 1 if gender.lower() == 'male' else 0  # 1 for male, 0 for female
    features = np.array([[animal_type_numeric, breed_encoded, age, gender_numeric, weight]])
    return longevity_model.predict(features)[0]

def predict_grooming_frequency(animal_type, breed_encoded, age, gender, weight):
    animal_type_numeric = 1 if animal_type.lower() == 'dog' else 0
    gender_numeric = 1 if gender.lower() == 'male' else 0
    features = np.array([[animal_type_numeric, breed_encoded, age, gender_numeric, weight]])
    return grooming_model.predict(features)[0]

def predict_lifetime_cost(animal_type, breed_encoded, age, gender, weight):
    animal_type_numeric = 1 if animal_type.lower() == 'dog' else 0
    gender_numeric = 1 if gender.lower() == 'male' else 0
    features = np.array([[animal_type_numeric, breed_encoded, age, gender_numeric, weight]])
    return lifetime_cost_model.predict(features)[0]

def predict_food_cost(animal_type, breed_encoded, age, gender, weight):
    animal_type_numeric = 1 if animal_type.lower() == 'dog' else 0
    gender_numeric = 1 if gender.lower() == 'male' else 0
    features = np.array([[animal_type_numeric, breed_encoded, age, gender_numeric, weight]])
    return max(food_cost_model.predict(features)[0], 100)  # Ensure minimum food cost is 100

# Function to predict diseases
def predict_diseases(animal_type, breed_encoded, age, gender, weight, appetite_loss, vomiting, diarrhea, coughing, labored_breathing, lameness, skin_lesions, nasal_discharge, eye_discharge, body_temperature, heart_rate):
    animal_type_numeric = 1 if animal_type.lower() == 'dog' else 0
    gender_numeric = 1 if gender.lower() == 'male' else 0
    features = np.array([[animal_type_numeric, breed_encoded, age, gender_numeric, weight,
                          appetite_loss, vomiting, diarrhea, coughing, labored_breathing, lameness,
                          skin_lesions, nasal_discharge, eye_discharge, body_temperature, heart_rate]])
    return disease_model.predict(features)[0]





# Kivy Screen for pet information input and prediction display
import re
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty

class PetInfoScreen(Screen):
    breed_input = ObjectProperty(None)
    animal_type_layout = ObjectProperty(None)
    age_input = ObjectProperty(None)
    gender_input = ObjectProperty(None)
    weight_input = ObjectProperty(None)

    longevity_label = ObjectProperty(None)
    grooming_label = ObjectProperty(None)
    lifetime_cost_label = ObjectProperty(None)
    food_cost_label = ObjectProperty(None)

    prediction_message = StringProperty("")

    def __init__(self, **kwargs):
        super(PetInfoScreen, self).__init__(**kwargs)

    def on_enter(self):
        pass

    # Validation function for Gender and Breed (Only letters, auto-capitalization)
    def validate_text(self, instance, value):
        filtered_text = ''.join([char for char in value if char.isalpha() or char == ' '])
        if filtered_text:
            filtered_text = filtered_text[0].upper() + filtered_text[1:]  # Capitalize first letter
        instance.text = filtered_text

    # Validation function for Age and Weight (Only numbers, max 2 digits)
    def validate_numeric(self, instance, value):
        filtered_text = ''.join([char for char in value if char.isdigit()])[:2]  # Restrict to 2 digits
        instance.text = filtered_text

    def submit_form(self):
        # Retrieve user inputs
        breed = self.breed_input.text.strip()
        try:
            breed_encoded = encode_breed(breed)
        except ValueError as e:
            print(f"Error encoding breed: {e}")
            self.prediction_message = "Breed encoding failed."
            return

        # Check selected animal type
        if self.ids.dog_button.state == 'down':
            animal_type = "Dog"
        elif self.ids.cat_button.state == 'down':
            animal_type = "Cat"
        else:
            animal_type = ""

        age = self.age_input.text.strip()
        gender = self.gender_input.text.strip()
        weight = self.weight_input.text.strip()

        # **Validation: Ensure all fields are filled**
        if not all([breed, animal_type, age, gender, weight]):
            self.prediction_message = "Please fill in all fields."
            return

        # **Validation: Age and Weight must be numbers**
        try:
            age = int(age)
            weight = int(weight)
        except ValueError:
            self.prediction_message = "Age and weight must be numbers."
            return

        # **Validation: Age and Weight should be max 2 digits**
        if len(str(age)) > 2 or len(str(weight)) > 2:
            self.prediction_message = "Age and Weight must be max 2 digits!"
            return

        # Encode the breed
        breed_encoded = encode_breed(breed)

        if breed_encoded != -1:
            # Make predictions using model functions
            longevity = predict_longevity(animal_type, breed_encoded, age, gender, weight)
            grooming_frequency = predict_grooming_frequency(animal_type, breed_encoded, age, gender, weight)
            lifetime_cost = predict_lifetime_cost(animal_type, breed_encoded, age, gender, weight)
            food_cost = predict_food_cost(animal_type, breed_encoded, age, gender, weight)

            # ✅ **Fix: Adjust food cost as per conditions**
            if food_cost > 500:
                food_cost -= 200
            elif food_cost > 400:
                food_cost -= 100

            # ✅ **Fix: Adjust lifetime cost as per conditions**
            if lifetime_cost > 20000:
                lifetime_cost -= 10000
            elif 10000 < lifetime_cost <= 20000:
                lifetime_cost -= 5000
            # ≤ 10,000 → No change

            # Update prediction labels with results
            self.longevity_label.text = f"Predicted Longevity: {longevity:.2f} years"
            
            if grooming_frequency == 1:
                grooming_text = "Daily grooming at home + Monthly once professional grooming"
            elif grooming_frequency == 3:
                grooming_text = "Twice a week grooming at home + Two months once professional grooming"
            elif grooming_frequency == 7:
                grooming_text = "Once a week grooming at home + Three months once professional grooming"
            elif grooming_frequency == 14:
                grooming_text = "Once every two weeks grooming at home + Four months once professional grooming"
            else:
                grooming_text = "Unknown frequency"

            self.grooming_label.text = f"Predicted Grooming Frequency: {grooming_text}"
            self.lifetime_cost_label.text = f"Predicted Lifetime Cost: ${lifetime_cost:.2f}"
            self.food_cost_label.text = f"Predicted Food Cost: ${food_cost:.2f} per year"

            # Common food suggestions
            common_foods = "Common foods: Beef, Chicken, Dairy, Fish, Eggs, Grains (wheat, Soya, corn), Vegetables like sweet potatoes, carrots, and pumpkin"
            self.ids.common_foods_label.text = common_foods  # Set text for the label
        
            self.prediction_message = ""

    def go_back(self):
        # Go back to the main screen
        self.manager.current = "main"

    def go_to_diseases(self):
        self.manager.current = "diseases"









from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox  

class DiseasesScreen(Screen):
    # UI Components
    disease_prediction_result = ObjectProperty(None)  # Label for showing the result
    prediction_message = StringProperty("")  # Message for missing input handling

    def on_kv_post(self, base_widget):
        """Assign UI elements after KV file is loaded."""
        # ✅ Ensure correct assignment of input fields
        self.disease_prediction_result = self.ids.disease_prediction_result  
        self.breed_input = self.ids.breed_input
        self.age_input = self.ids.age_input
        self.gender_input = self.ids.gender_input
        self.weight_input = self.ids.weight_input
        self.body_temperature_input = self.ids.body_temperature_input
        self.heart_rate_input = self.ids.heart_rate_input

        # ✅ Assign CheckBox fields properly
        self.appetite_loss_input = self.ids.appetite_loss_input
        self.vomiting_input = self.ids.vomiting_input
        self.diarrhea_input = self.ids.diarrhea_input
        self.coughing_input = self.ids.coughing_input
        self.labored_breathing_input = self.ids.labored_breathing_input
        self.lameness_input = self.ids.lameness_input
        self.skin_lesions_input = self.ids.skin_lesions_input
        self.nasal_discharge_input = self.ids.nasal_discharge_input
        self.eye_discharge_input = self.ids.eye_discharge_input

    def get_input_value(self, input_field):
        """Helper function to get checkbox input values (1 if checked, 0 otherwise)."""
        if isinstance(input_field, CheckBox):  # ✅ Ensure it's a CheckBox
            return 1 if input_field.active else 0
        return 0  # Default to 0 if input_field is not a CheckBox

    def get_text_input_value(self, input_field):
        """Helper function to safely get numeric values from text input fields."""
        if isinstance(input_field, TextInput):  # ✅ Ensure it's a TextInput
            try:
                return float(input_field.text.strip()) if input_field.text.strip() else 0.0
            except ValueError:
                return 0.0  # Return default if conversion fails
        return 0.0  # Default value if not a TextInput

    def submit_form(self):
        """Collects form data and predicts diseases."""
        breed = self.breed_input.text.strip()
        if not breed:
            self.prediction_message = "Please enter the breed."
            return

        try:
            breed_encoded = encode_breed(breed)  # Ensure encode_breed function exists
        except ValueError as e:
            print(f"Error encoding breed: {e}")
            self.prediction_message = "Breed encoding failed."
            return

        # Determine animal type
        animal_type = None
        if self.ids.dog_button.state == 'down':
            animal_type = "Dog"
        elif self.ids.cat_button.state == 'down':
            animal_type = "Cat"

        if animal_type is None:
            self.prediction_message = "Please select an animal type."
            return

        age = self.get_text_input_value(self.age_input)
        gender = self.gender_input.text.strip()
        weight = self.get_text_input_value(self.weight_input)

        # Validate user input
        if not all([breed, animal_type, age, gender, weight]):
            self.prediction_message = "Please fill in all required fields."
            return

        if not isinstance(age, (int, float)) or age <= 0:
            self.prediction_message = "Age must be a positive number."
            return

        if not isinstance(weight, (int, float)) or weight <= 0:
            self.prediction_message = "Weight must be a positive number."
            return

        # ✅ Retrieve symptom inputs correctly
        appetite_loss = self.get_input_value(self.appetite_loss_input)
        vomiting = self.get_input_value(self.vomiting_input)
        diarrhea = self.get_input_value(self.diarrhea_input)
        coughing = self.get_input_value(self.coughing_input)
        labored_breathing = self.get_input_value(self.labored_breathing_input)
        lameness = self.get_input_value(self.lameness_input)
        skin_lesions = self.get_input_value(self.skin_lesions_input)
        nasal_discharge = self.get_input_value(self.nasal_discharge_input)
        eye_discharge = self.get_input_value(self.eye_discharge_input)

        body_temperature = self.get_text_input_value(self.body_temperature_input)
        heart_rate = self.get_text_input_value(self.heart_rate_input)

        # ✅ Call prediction function
        try:
            disease = predict_diseases(
                animal_type, breed_encoded, age, gender, weight,
                appetite_loss, vomiting, diarrhea, coughing,
                labored_breathing, lameness, skin_lesions,
                nasal_discharge, eye_discharge, body_temperature, heart_rate
            )
        except Exception as e:
            print(f"Error during prediction: {e}")
            self.prediction_message = "An error occurred during prediction."
            return

        # ✅ Update result label properly
        if disease:
            self.disease_prediction_result.text = f"Predicted Disease: {disease}"
        else:
            self.disease_prediction_result.text = "Disease prediction failed."

        self.prediction_message = ""  # ✅ Remove incorrect syntax

        def go_back(self):
            """ Navigate back to the main screen. """
            self.manager.current = "main" 






from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
import pandas as pd
import joblib  # For loading the trained model

# Load the trained adoption model and breed encoder
adoption_model = joblib.load("C:\\pet_care_app\\models\\adoption.pkl")
breed_encoder = joblib.load("C:\\pet_care_app\\models\\breed_encoder.pkl")  # Load pre-fitted encoder

class FindYourPetMatch(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Spinner for stay selection
        self.stay_spinner = Spinner(
            text="Select Stay Type",
            values=("indoor", "outdoor", "both"),
            size_hint=(1, 0.2)
        )
        self.add_widget(Label(text="Select Stay Type:"))
        self.add_widget(self.stay_spinner)

        # Spinner for selecting animal type
        self.animal_spinner = Spinner(
            text="Select Animal Type",
            values=("dog", "cat"),
            size_hint=(1, 0.2)
        )
        self.add_widget(Label(text="Select Animal Type:"))
        self.add_widget(self.animal_spinner)

        # Spinner for space requirement
        self.space_label = Label(text="Space Requirement (sqft):")
        self.add_widget(self.space_label)
        self.space_spinner = Spinner(
            text="100",
            values=["100", "200", "300", "400"],
            size_hint=(1, 0.2)
        )
        self.add_widget(self.space_spinner)

        # Spinner for pet height
        self.height_label = Label(text="Pet Height (in inches):")
        self.add_widget(self.height_label)
        self.height_spinner = Spinner(
            text="4",
            values=["4", "6", "8", "10"],
            size_hint=(1, 0.2)
        )
        self.add_widget(self.height_spinner)

        # Button to predict breed
        self.predict_button = Button(text="Predict Breed", size_hint=(1, 0.2))
        self.predict_button.bind(on_press=self.predict_breed)
        self.add_widget(self.predict_button)

        # Label to display the prediction
        self.result_label = Label(text="Predicted Breed: ", size_hint=(1, 0.2))
        self.add_widget(self.result_label)

    def predict_breed(self, instance):
        # Mappings for categorical values
        stay_mapping = {'indoor': 0, 'outdoor': 1, 'both': 2}
        animal_mapping = {'dog': 1, 'cat': 0}  # Assuming 'dog' is encoded as 1

        # Prepare input data
        X_test = pd.DataFrame({
            'stay': [stay_mapping[self.stay_spinner.text]],  # Directly map stay type
            'Space requirement': [int(self.space_spinner.text)],
            'height(inches)': [int(self.height_spinner.text)],
            'Animal_Type': [animal_mapping[self.animal_spinner.text]]
        })

        # Predict the breed index
        predicted_breed_index = adoption_model.predict(X_test)

        # Convert numeric prediction back to breed name
        predicted_breed = breed_encoder.inverse_transform(predicted_breed_index)[0]

        # Update UI with prediction
        self.result_label.text = f"Predicted Breed: {predicted_breed}"


    

class MyApp(App):
    def build(self):
        return FindYourPetMatch()  # Corrected return


















# Kivy App Class
class PetApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SignInScreen(name="signin"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="sign_up"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(PetInfoScreen(name="pet_info"))
        sm.add_widget(FindYourPetMatchScreen(name="pet_match"))
        sm.add_widget(DiseasesScreen(name="diseases"))
        sm.add_widget(ChatbotScreen(name="chatbot"))
        sm.current = "home"
        return sm

if __name__ == "__main__":
    PetApp().run()