from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import json
import os

# File paths and settings
data_file = "user_data.json"
land_rentals_file = "land_rentals.json"
marketplace_file = "marketplace.json"

# Initialize files if not present
if not os.path.exists(data_file):
    with open(data_file, "w") as file:
        json.dump({}, file)

if not os.path.exists(land_rentals_file):
    with open(land_rentals_file, "w") as file:
        json.dump([], file)

if not os.path.exists(marketplace_file):
    with open(marketplace_file, "w") as file:
        json.dump([], file)

# File loading and saving functions
def load_user_data():
    with open(data_file, "r") as file:
        return json.load(file)

def save_user_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

def load_land_rentals():
    with open(land_rentals_file, "r") as file:
        return json.load(file)

def save_land_rentals(data):
    with open(land_rentals_file, "w") as file:
        json.dump(data, file, indent=4)

def load_marketplace():
    with open(marketplace_file, "r") as file:
        return json.load(file)

def save_marketplace(data):
    with open(marketplace_file, "w") as file:
        json.dump(data, file, indent=4)

# Screens
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Welcome to the App")
        login_btn = Button(text="Login", size_hint=(1, 0.2))
        login_btn.bind(on_release=self.switch_to_login)
        signup_btn = Button(text="Sign Up", size_hint=(1, 0.2))
        signup_btn.bind(on_release=self.switch_to_signup)
        layout.add_widget(label)
        layout.add_widget(login_btn)
        layout.add_widget(signup_btn)
        self.add_widget(layout)

    def switch_to_login(self, instance):
        self.manager.current = "login"

    def switch_to_signup(self, instance):
        self.manager.current = "signup"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text="Username")
        self.password_input = TextInput(hint_text="Password", password=True)
        login_btn = Button(text="Login")
        login_btn.bind(on_release=self.login)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            self.manager.current = "dashboard"
        else:
            self.add_widget(Label(text="Invalid login credentials", size_hint=(1, 0.2)))

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text="Username")
        self.password_input = TextInput(hint_text="Password", password=True)
        signup_btn = Button(text="Sign Up")
        signup_btn.bind(on_release=self.signup)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(signup_btn)
        self.add_widget(layout)

    def signup(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        user_data = load_user_data()
        if username in user_data:
            self.add_widget(Label(text="Username already exists", size_hint=(1, 0.2)))
        else:
            user_data[username] = {"password": password}
            save_user_data(user_data)
            self.manager.current = "login"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Dashboard")
        features = [
            "Soil Mapping by Region",
            "Multi-Language Support",
            "Voice Interface for Non-Readers/Writers",
            "Regional Climate Patterns with Crop Recommendations",
            "Land Leasing/Renting Options",
            "Buy/Sell Marketplace",
        ]
        scroll = ScrollView(size_hint=(1, 0.8))
        feature_list = BoxLayout(orientation='vertical', size_hint_y=None)
        feature_list.bind(minimum_height=feature_list.setter('height'))

        for feature in features:
            feature_list.add_widget(Label(text=feature, size_hint_y=None, height=40))

        scroll.add_widget(feature_list)
        logout_btn = Button(text="Logout", size_hint=(1, 0.2))
        logout_btn.bind(on_release=self.switch_to_home)
        layout.add_widget(label)
        layout.add_widget(scroll)
        layout.add_widget(logout_btn)
        self.add_widget(layout)

    def switch_to_home(self, instance):
        self.manager.current = "home"

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        return sm

if __name__ == "__main__":
    MyApp().run()