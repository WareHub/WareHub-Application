import kivy
import requests


kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.button import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.listview import ListItemButton
import json




class LoginScreen(Screen):

    def login(self):
    	self.manager.current = 'manager_screen'
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
    		except requests.exceptions.ConnectionError:
    			message = 'Check your internet connetcion'
    	else:
    		message = 'please enter your id and password'




class Student(ListItemButton):
	pass





class ManagerScreen(Screen):
	def getStudents(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/getstudents')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend([s[1]])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'

	def getTechs(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/gettechs')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend([s[1]])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'



class ScreenManagment(ScreenManager):
	login_screen = ObjectProperty(None)
	manager_screen = ObjectProperty(None)





    
class WareHub1App(App):

    def build(self):
        return ScreenManagment(transition = NoTransition())


wH = WareHub1App()
wH.run()
