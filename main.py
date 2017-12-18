import kivy
import requests

import sys

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
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.spinner import Spinner
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.core.window import Window

import json
import datetime


ID = 0
myPassword = ''
myType = -1
textofDeviceStudent=""
deviceID = 0
devices_names ={'PCs':'5','Data shows':'2','Microphones':'1','Kits':'3','Arduinos':'4','Bread boards':'6','ICs':'7'}
additionScreenMode = -1

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
    				self.manager.current = 'clear_screen'
    				self.manager.current = 'manager_screen'
    			elif isLoggedin == 1:
    				self.manager.current = 'clear_screen'
    				self.manager.current = 'student_screen'
    			elif isLoggedin == 2:
    				self.manager.current = 'clear_screen'
    				self.manager.current = 'tech_screen'
    			else:
    				message = 'ID or password is not correct'
    				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
    				popup.open()
    		except ValueError:
    			message = 'invalid id'
    			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
    			popup.open()

    		except requests.exceptions.ConnectionError:
    			message = 'Check your internet connetcion'
    			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
    			popup.open()
    	else:
    		message = 'please enter your id and password'
    		popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
    		popup.open()




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
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()
		

	def getStudents(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/getstudents')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend(['ID: {}\n{}\nPhone: {}\nIsTA: {}     Points: {}'.format(s[0], s[1], s[2], s[3], s[4])])
				self.my_list._trigger_reset_populate()
			self.mode = 0
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

	def getTechs(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/gettechs')
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			for s in data:
				self.my_list.adapter.data.extend(['ID: {}\n{}\nPhone: {}\nPoints: {}'.format(s[0], s[1], s[2], s[3])])
				self.my_list._trigger_reset_populate()
			self.mode = 0
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()





class DeviceStudentScreen(Screen):
	def on_pre_enter(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/getdevicereviews/{}'.format(deviceID))
			data = json.loads(data.text)
			self.listonedevice.adapter.data = []
			strpre="Time: {}\nOpinion: {}\nRate: {}"
			for s in data:
				self.listonedevice.adapter.data.extend([strpre.format(str(s[2]),str(s[3]),str(s[4]))])
				self.listonedevice._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
	


	def addReview(self):
		text = self.ids.review_textinput.text
		rate = self.ids.rate_spinner.text
		if rate != 'Rate':
			try:
				currentDate = datetime.datetime.now()
				payload = {'': [str(ID), str(deviceID), str(currentDate), text, rate]}
				requests.post('http://warehub-api.azurewebsites.net/insertreview', data = payload)
				payload = {'id': str(deviceID), 'r': rate}
				requests.post('http://warehub-api.azurewebsites.net/update_devicerate', data = payload)
				self.on_pre_enter()
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
		else:
			message = 'please choose a rate'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


	def demandDevice(self):
		months = self.ids.months_textinput.text
		days = self.ids.days_textinput.text
		hours = self.ids.hours_textinput.text
		minutess = self.ids.minutess_textinput.text
		monthe = self.ids.monthe_textinput.text
		daye = self.ids.daye_textinput.text
		houre = self.ids.houre_textinput.text
		minutese = self.ids.minutese_textinput.text
		if len(months) > 0 and len(days) > 0 and len(hours) > 0 and len(minutess) > 0 and len(monthe) > 0 and len(daye) > 0 and len(houre) > 0 and len(minutese) > 0:
			try:
				sDate1 = int(months)
				sDate2 = int(days)
				sDate3 = int(hours)
				sDate4 = int(minutess)
				eDate1 = int(monthe)
				eDate2 = int(daye)
				eDate3 = int(houre)
				eDate4 = int(minutese)
				currentYear = datetime.datetime.now().year
				startDate = datetime.datetime(currentYear, sDate1, sDate2, sDate3, sDate4)
				endDate = datetime.datetime(currentYear, eDate1, eDate2, eDate3, eDate4)
				payload = {'': [str(ID), str(deviceID), str(startDate), str(endDate)]}
				data = requests.post('http://warehub-api.azurewebsites.net/insertdemand', data = payload)
			except ValueError:
				message = 'please enter logical values'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
		else:
			message = "please enter all values"
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()




class StudentScreen(Screen):
	selected_device=""
	##set function to do some thing you need when select (name dosen't effect)
	def show_selected_value_spinner(self,spinner, text):
		self.selected_device=text
		self.getDevices()

	def my_list_functionalities(self,ad):
		if self.mode == 0:
			try:
				global textofDeviceStudent,devices_names, deviceID
				textofDeviceStudent=str(ad.selection[0].text)+str(devices_names[self.selected_device])
				deviceID = int(textofDeviceStudent[14:22])
				self.manager.current = 'clear_screen'
				self.manager.current = 'device_student_screen'
				
			except:
				pass
		elif self.mode == 1:
			if ad.selection:
				text = self.my_list.adapter.selection[0].text
				self.deleteDemand(text)
				



	def on_pre_enter(self):
		global devices_names
		self.ids.Devices_Spinner.values = devices_names
		self.ids.Devices_Spinner.bind(text=self.show_selected_value_spinner)

	def getDevices(self):
		try:
			num=devices_names[self.selected_device]
			data = requests.get('http://warehub-api.azurewebsites.net/retrive_devices/{}'.format(num))
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			strpre="ID: {}\nType: {}    location: {}\nstate: {}    rate: {}"
			self.my_list.adapter.bind(on_selection_change=self.my_list_functionalities)
			self.mode = 0
			for s in data:
				self.my_list.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],s[4]/s[5])])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

	def getDemands(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/retrievedemand_st/{}'.format(ID))
			data = json.loads(data.text)
			self.my_list.adapter.bind(on_selection_change=self.my_list_functionalities)
			self.mode = 1
			self.my_list.adapter.data = []
			for item in data:
				self.my_list.adapter.data.extend(['ID: {}\nST: {}\nET: {}\nReserved: {}   In Use: {}'.format(item[1], item[2], item[3], item[4], item[5])])
				self.my_list._trigger_reset_populate()
			popup = Popup(title='', content=Label(text='Click on any demand to be deleted'), size_hint=(None, None), size = (500, 200))
			popup.open()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			

	def deleteDemand(self, text):
		try:
			text1 = text.split('\n')
			dID = text1[0][3:]
			sTime = text1[1][3:]
			payload = {'': [str(ID), dID, sTime]}
			requests.post('http://warehub-api.azurewebsites.net/deletedemand_st', data = payload)
			self.my_list.adapter.data.remove(text)
			self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


	

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
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()
					return
				payload = {'': [str(typeUser), name, password, phone, str(isTA), str(points)]}
				print (payload)
				requests.post('http://warehub-api.azurewebsites.net/insertuser', data = payload)
			except ValueError:
				message = 'Enter valid information'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
		else:
			message = 'Please enter all information of user'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


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
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

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
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
		else:
			message = 'please enter your password and phone'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


	def backButton(self):
		if myType == 0:
			self.manager.current = 'clear_screen'
			self.manager.current = 'manager_screen'
		elif myType == 1:
			self.manager.current = 'clear_screen'
			self.manager.current = 'student_screen'
		else:
			self.manager.current = 'clear_screen'
			self.manager.current = 'tech_screen'

class DeviceTechScreen(Screen):
	def on_pre_enter(self):
		try:
			self.id=textofDeviceStudent.split(" type")[0][14:]
			num=textofDeviceStudent[-1:]
			print(textofDeviceStudent,num)
			self.id=num*1000000+id
			data = requests.get('http://warehub-api.azurewebsites.net/getdevicereviews/{}'.format(id))
			data = json.loads(data.text)
			self.ids.one_device_Tech.adapter.data = []
			self.ids.one_device_Tech.adapter.data.extend([textofDeviceStudent[:-1]])
			strpre="time:{} opinion:{} rate:{}"
			for s in data:
				self.ids.one_device_Tech.adapter.data.extend([str(s[2]),str(s[3]),str(s[4])])
				self.ids.one_device_Tech._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


class TechScreen(Screen):
	selected_device=""
	##set function to do some thing you need when select (name dosen't effect)
	def show_selected_value_spinner(self,spinner, text):
		self.selected_device=text
		self.getDevices()

	def my_list_functionalities(self,ad):
		if self.mode == 0:
			try:
				global textofDeviceStudent,devices_names, deviceID
				textofDeviceStudent=str(ad.selection[0].text)+str(devices_names[self.selected_device])
				deviceID = int(textofDeviceStudent[14:22])
				self.manager.current = 'clear_screen'
				self.manager.current = 'device_tech_screen'
				
			except:
				pass
		elif self.mode == 1:
			if ad.selection:
				text = self.tech_list_view.adapter.selection[0].text
				try:
					text1 = text.split('\n')
					sID = text1[0][5:]
					dID = text1[1][5:]
					sDate = text1[2][4:]
					payload = {'': [sID, dID, sDate]}
					requests.post('http://warehub-api.azurewebsites.net/setinuse', data = payload)
				except requests.exceptions.ConnectionError:
					message = 'check your internet connection'
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()



	def on_pre_enter(self):
		global devices_names
		self.ids.Devices_Tech_Spinner.values = devices_names
		self.ids.Devices_Tech_Spinner.bind(text=self.show_selected_value_spinner)

	def getDevices(self):
		try:
			num=devices_names[self.selected_device]
			data = requests.get('http://warehub-api.azurewebsites.net/retrive_devices/{}'.format(num))
			data = json.loads(data.text)
			self.mode = 0
			self.tech_list_view.adapter.data = []
			strpre="ID: {}\nType: {}    location:{}\nstate: {}     rate: {}"
			self.tech_list_view.adapter.bind(on_selection_change=self.my_list_functionalities)
			for s in data:
				self.tech_list_view.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],s[4]/s[5])])
				self.tech_list_view._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

	def getDemands(self):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/retrievedemand_tech/{}'.format(ID))
			data = json.loads(data.text)
			self.tech_list_view.adapter.bind(on_selection_change=self.my_list_functionalities)
			self.mode = 1
			self.tech_list_view.adapter.data = []
			for item in data:
				self.tech_list_view.adapter.data.extend(['sID: {}\ndID: {}\nST: {}\nET: {}\nReserved: {}   In Use: {}'.format(item[0], item[1], item[2], item[3], item[4], item[5])])
				self.tech_list_view._trigger_reset_populate()
			popup = Popup(title='', content=Label(text='Click on any demand to Accept it'), size_hint=(None, None), size = (500, 200))
			popup.open()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


	def addOS(self):
		global additionScreenMode
		additionScreenMode = 0
		self.manager.current = 'clear_screen'
		self.manager.current = 'addition_screen'

	def addSoftware(self):
		global additionScreenMode
		additionScreenMode = 1
		self.manager.current = 'clear_screen'
		self.manager.current = 'addition_screen'


	def addICType(self):
		global additionScreenMode
		additionScreenMode = 2
		self.manager.current = 'clear_screen'
		self.manager.current = 'addition_screen'



class ClearScreen(Screen):
	pass






class AddDeviceScreen(Screen):
	pass





class AdditionScreen(Screen):
	def on_pre_enter(self):
		if additionScreenMode == 2:
			self.ids.name_text.hint_text = 'Code'
		else:
			self.ids.name_text.hint_text = 'Name'



	def add(self):
		thisName = self.ids.name_text.text
		link = self.ids.link_text.text
		if len(thisName)>0 and len(link)>0:
			if additionScreenMode == 0:
				try:
					payload = {'name':thisName, 'link': link}
					requests.post('http://warehub-api.azurewebsites.net/add_os', data = payload)
				except requests.exceptions.ConnectionError:
					message = 'Check your internet connetcion'
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()
			elif additionScreenMode == 1:
				try:
					payload = {'name':thisName, 'link': link}
					requests.post('http://warehub-api.azurewebsites.net/add_software', data = payload)
				except requests.exceptions.ConnectionError:
					message = 'Check your internet connetcion'
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()
			elif additionScreenMode == 2:
				try:
					payload = {'code':thisName, 'gate': link}
					requests.post('http://warehub-api.azurewebsites.net/add_ictype', data = payload)
				except requests.exceptions.ConnectionError:
					message = 'Check your internet connetcion'
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()
		else:
			message = 'please enter your id and password'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()






class ScreenManagment(ScreenManager):
	login_screen = ObjectProperty(None)
	manager_screen = ObjectProperty(None)
	clear_screen = ObjectProperty(None)





    
class WareHub1App(App):
    
    def build(self):
        return ScreenManagment(transition = NoTransition())


wH = WareHub1App()
wH.run()
