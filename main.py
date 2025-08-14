from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from signin import SignInScreen  # Correctly import the SignInScreen class from signin.py
from signin import LoginScreen
from signin import SignUpScreen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
 
from signin import MainScreen  
from signin import PetInfoScreen
from signin import FindYourPetMatchScreen

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        # Main layout for the screen
        self.layout = FloatLayout()

        # Top bar (10% of the screen) with white background
        with self.canvas.before:
            self.top_bar_color = Color(1, 1, 1, 1)  # White color
            self.top_bar = Rectangle(size=(self.width, self.height * 0.1), pos=(0, self.height * 0.9))
        self.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(
    text="[b]PAWSITIVE CARE[/b]",  # Bold the text
    font_size=60,  # Adjust font size as needed
    markup=True,  # Allow bold text using BBCode
    color=(0, 0, 0, 1),  # Black text color
    size_hint=(None, None),
    size=(self.width * 0.4, self.height * 0.1),  # Adjust size
    pos_hint={"center_x": 0.5, "top": 0.95}  # Center horizontally and position at the top
)
        self.add_widget(title_label)

        # Home Button
        self.home_button = Button(
            text="Home",
            size_hint=(None, None),  # To specify the exact size
            size=(200, 50),  # Set the button size to 200x50
            pos_hint={"x": 0.75, "y": 0.92},
            background_color=(0.2, 0.5, 0.8, 1),  # Background color (blue)
            on_press=self.home,  # Call the home method when the button is pressed
        )
        self.layout.add_widget(self.home_button)

        # Login Button
        self.login_button = Button(
            text="Login",
            size_hint=(None, None),  # To specify the exact size
            size=(200, 50),  # Set the button size to 200x50
            pos_hint={"x": 0.87, "y": 0.92},
            background_color=(0.2, 0.5, 0.8, 1),  # Background color (blue)
            on_press=self.switch_to_login,  # Call the switch_to_login method when the button is pressed
        )
        self.layout.add_widget(self.login_button)

        # Slideshow area (90% of the screen)
        self.image_index = 0
        self.image_paths = [
            "C:/pet_care_app/frontdogcat.jpeg",
            "C:/pet_care_app/frontdogcat2.jpeg",
            "C:/pet_care_app/frontdog.jpeg",
            "C:/pet_care_app/frontcat.jpeg",
        ]
        self.slideshow_image = Image(
            source=self.image_paths[self.image_index],
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 0.9),
            pos_hint={"x": 0, "y": 0},
        )
        self.layout.add_widget(self.slideshow_image)

        # Schedule image change every 3 seconds
        Clock.schedule_interval(self.change_image, 3)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        # Update the top bar's rectangle when resizing
        self.top_bar.size = (self.width, self.height * 0.1)
        self.top_bar.pos = (0, self.height * 0.9)

    def change_image(self, dt):
        # Update the image in the slideshow
        self.image_index = (self.image_index + 1) % len(self.image_paths)
        self.slideshow_image.source = self.image_paths[self.image_index]

    def switch_to_login(self, instance):
        # Navigate to the SignIn screen
        self.manager.current = "signin"

    def home(self, instance):
        # Action for the home button, if needed
        print("Home button pressed")


class PetCareApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SignInScreen(name="signin"))  # Ensure that SignInScreen is correctly added
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="sign_up"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(PetInfoScreen(name="pet_info")) 
        sm.add_widget(FindYourPetMatchScreen(name="pet_match"))
        
        
        return sm


if __name__ == "__main__":
    PetCareApp().run()
