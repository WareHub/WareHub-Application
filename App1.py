import kivy
import requests


kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput

class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def login(self):
    	userName = self.ids.username_text.text
    	password = self.ids.password_text.text
    	if len(userName)>0 and len(password)>0:
    		try:
    			idUser = int(userName)
    			payload = {'': [userName, password]}
    			isLoggedin = requests.post('http://warehub-api.azurewebsites.net/login', data = payload)
    			self.ids.username_text.text = str(isLoggedin.text)	
    		except ValueError:
    			message = 'invalid id'
    	else:
    		message = 'please enter your id and password'


class MainMenu():
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
    
class WareHub1App(App):

    def build(self):
        return LoginScreen()


wH = WareHub1App()
wH.run()
