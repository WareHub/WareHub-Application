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
from kivy.uix.checkbox import CheckBox

from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp

import json



ID = 0
myPassword = ''
myType = -1

class LoginScreen(Screen):

    def login(self):
    	userName = self.ids.username_text.text
    	password = self.ids.password_text.text
    	#self.manager.current = 'student_screen'
    	if len(userName)>0 and len(password)>0:
    		try:
    			idUser = int(userName)
    			payload = {'': [userName, password]}
    			isLoggedin = requests.post('http://warehub-api.azurewebsites.net/login', data = payload)

    			isLoggedin = int(isLoggedin.text)
    			global ID, myPassword, myType
    			ID = idUser
    			myPassword = password
    			myType = isLoggedin
    			if (isLoggedin == 0):
    				self.manager.current = 'manager_screen'
    			elif isLoggedin == 1:
    				self.manager.current = 'student_screen'
    			elif isLoggedin == 2:
    				self.manager.current = 'tech_screen'
    			else:
    				message = 'ID or password is not correct'
    		except ValueError:
    			message = 'invalid id'
    			print ('here')
    		except requests.exceptions.ConnectionError:
    			message = 'Check your internet connetcion'
    	else:
    		message = 'please enter your id and password'




class Student(ListItemButton):
	pass





class ManagerScreen(Screen):
	
	def deleteElement(self):
		if self.mode == 0:
			if self.my_list.adapter.selection:
				text = self.my_list.adapter.selection[0].text
				id = text[4:12]
				try:
					requests.delete('http://warehub-api.azurewebsites.net/deleteuser/{}'.format(id))
					self.my_list.adapter.data.remove(text)
					self.my_list._trigger_reset_populate()
				except requests.exceptions.ConnectionError:
					message = 'Check your internet connetcion'
		

	def getStudents(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/getstudents')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend(['ID: {}\nName: {}\nPhone: {}\nIsTA: {}     Points: {}'.format(s[0], s[1], s[2], s[3], s[4])])
				self.my_list._trigger_reset_populate()
			self.mode = 0
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'

	def getTechs(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/gettechs')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend(['ID: {}\nName: {}\nPhone: {}\nPoints: {}'.format(s[0], s[1], s[2], s[3])])
				self.my_list._trigger_reset_populate()
			self.mode = 0
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'


class StudentScreen(Screen):
	selected_device=""
	selected_one_device=""
	##set function to do some thing you need when select (name dosen't effect)
	def show_selected_value_spinner(self,spinner, text):
		self.selected_device=text
		self.getDevices()

	def show_selected_value_list(self,ad):
		print (ad.selection[0].text)	

	def on_pre_enter(self):
		self.devices_names={'PCs':'5','Data shows':'2','Microphones':'1','Kits':'3','Arduinos':'4','Bread boards':'6','ICs':'7'}
		self.ids.Devices_Spinner.values = self.devices_names
		self.ids.Devices_Spinner.bind(text=self.show_selected_value_spinner)

	def getDevices(self):
		try:
			num=self.devices_names[self.selected_device]
			data = requests.get('http://warehub-api.azurewebsites.net/retrive_devices/{}'.format(num))
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			strpre="device number:{} type:{} location:{} state:{} rate:{}"
			self.my_list.adapter.bind(on_selection_change=self.show_selected_value_list)
			for s in data:
				self.my_list.adapter.data.extend([strpre.format(s[0]%1000000,s[1],s[2],s[3],s[4]/s[5])])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'

	def getOneDevice(self):
		try:
			num=self.devices_names[self.selected_device]
			data = requests.get('http://warehub-api.azurewebsites.net/retrive_devices/{}'.format(num))
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			#strpre1="device number  type    location    state   rate"
			#self.my_list.adapter.data.extend([strpre1])
			#strpre="{}              {}      {}          {}      {}"
			strpre="device number:{} type:{} location:{} state:{} rate:{}"
			for s in data:
				self.my_list.adapter.data.extend([strpre.format(s[0]%1000000,s[1],s[2],s[3],s[4]/s[5])])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'

	



	

class AddUserScreen(Screen):
	def insertUser(self):
		name = self.ids.name_text.text
		password = self.ids.password_text.text
		phone = self.ids.phone_text.text
		points = self.ids.points_text.text
		if len(name)>0 and len(password)>0 and len(phone)>0 and len(points)>0:
			try:
				pointsI = int(points)
				phoneI = int(phone)
				isTA = 0
				if bool(self.ids.manager_radiobutton.active):
					typeUser = 0
				elif bool(self.ids.student_radiobutton.active):
					typeUser = 1
					isTA = int(self.ids.ta_checkbox.active)
				elif bool(self.ids.tech_radiobutton.active):
					typeUser = 2
				else:
					message = 'please enter user type'
					return
				payload = {'': [str(typeUser), name, password, phone, str(isTA), str(points)]}
				print (payload)
				requests.post('http://warehub-api.azurewebsites.net/insertuser', data = payload)
			except ValueError:
				message = 'Enter valid information'
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
		else:
			message = 'Please enter all information of user'


class UpdateInfoScreen(Screen):
	def on_pre_enter(self):
		try:
			if myType == 0:
				g = 'getmanager'
			elif myType == 1:
				g = 'getstudent'
			else:
				g = 'gettech'
			data = requests.get('http://warehub-api.azurewebsites.net/{}/{}'.format(g, ID))
			data = json.loads(data.text)
			print (ID)
			print (data)
			self.ids.password_text.text = myPassword
			self.ids.phone_text.text = str(data[0][2])
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'

	def updateInfo(self):
		password = self.ids.password_text.text
		phone = self.ids.phone_text.text
		if len(password) > 0 and len(phone) > 0:
			try:
				payload = {'': [str(myType), str(ID), password, phone]}
				requests.post('http://warehub-api.azurewebsites.net/updateinfo', data = payload)
				myPassword = password
			except requests.exceptions.ConnectionError:
				message = 'check your internet connection'
		else:
			message = 'please enter your password and phone'


	def backButton(self):
		if myType == 0:
			self.manager.current = 'manager_screen'
		elif myType == 1:
			self.manager.current = 'student_screen'
		else:
			self.manager.current = 'tech_screen'


class TechScreen(Screen):
	pass


class ScreenManagment(ScreenManager):
	login_screen = ObjectProperty(None)
	manager_screen = ObjectProperty(None)





    
class WareHub1App(App):
    
    def build(self):
        return ScreenManagment(transition = NoTransition())


wH = WareHub1App()
wH.run()
