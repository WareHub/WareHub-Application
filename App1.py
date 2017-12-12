import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput

class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

class MainMenu():
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
    
class WareHub1App(App):

    def build(self):
        return LoginScreen()


wH = WareHub1App()
wH.run()
