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


class GraphScreen(Screen):
	pass


class ManagerScreen(Screen):
	mode = -1

	def show_selected_value_spinner(self, sp, text):
		if text == 'rush hours':
			self.getStats('getrushhour')
		elif text == 'crowded days':
			self.getStats('getcrowded_day')
		elif text == 'PCs Demands':
			self.getStats('getmostdemanded_pcs')
		elif text == "ICs Demands":
			self.getStats('getmostdemanded_ic')
		elif text  == 'OS demands':
			self.getStats('getmostused_os')
		elif text  == 'Software demands':
			self.getStats('getmostused_software')
		elif text  == 'Complains':
			self.getStats('getcomplains')
		elif text  == 'PCs Uses':
			self.getStats('getmostused_pc')
		elif text  == 'ICs Uses':
			self.getStats('getmostused_ic')



	def getStats(self, text):
		try:
			data = requests.get('http://warehub-api.azurewebsites.net/{}'.format(text))
			data = json.loads(data.text)
			self.my_list.adapter.data = []
			if text == 'getrushhour':
				strpre="Time: {}\nDemands: {}"
			elif text == 'getcrowded_day':
				strpre = "Date: {}\nDemands: {}"
			elif text == 'getmostdemanded_pcs':
				strpre = "ID: {}\nDemands: {}"
			elif text == "getmostdemanded_ic":
				 strpre = "CODE: {}\nDemands: {}"
			elif text == "getmostused_os":
				 strpre = "Name: {}\nDemands: {}"
			elif text == "getmostused_software":
				 strpre = "Name: {}\nDemands: {}"
			elif text == "getcomplains":
				 strpre = "ID: {}\nnum Complains: {}"
			elif text == "getmostused_pc":
				 strpre = "ID: {}\nUses: {}"
			elif text == "getmostused_ic":
				 strpre = "CODE: {}\nnUses: {}"


			for s in data:
				self.my_list.adapter.data.extend([strpre.format(s[0],s[1])])
				self.my_list._trigger_reset_populate()
		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()


	def back(self, instance):
		self.manager.current = 'clear_screen'
		self.manager.current = 'manager_screen'

	def on_pre_enter(self):
		self.ids.stats_spinner.bind(text=self.show_selected_value_spinner)
	
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
				deviceID = int(textofDeviceStudent[4:12])
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
			strpre="ID: {}\nType: {}\nlocation: {}\nstate: {}\nrate: {}"
			self.my_list.adapter.bind(on_selection_change=self.my_list_functionalities)
			self.mode = 0
			for s in data:
				try:
					self.my_list.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],s[4]/s[5])])
				except:
					self.my_list.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],'Not Rated')])
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
				self.my_list.adapter.data.extend(['ID: {}\nST: {}\nET: {}\nReserved: {}\nIn Use: {}'.format(item[1], item[2][0:19], item[3][0:19], item[4], item[5])])
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
				return 
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
				return
		else:
			message = 'Please enter all information of user'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return
		message = 'Done !'
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
		self.manager.current = 'clear_screen'
		self.manager.current = 'save_screen'

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
	mode = -1
	
	def deleteElement(self):
		if self.mode == 0:
			if self.tech_list_view.adapter.selection:
				text = self.tech_list_view.adapter.selection[0].text
				id = text[4:12]
				try:
					payload = {'id':[id]}
					requests.post('http://warehub-api.azurewebsites.net/remove_Device', data = payload)
					self.tech_list_view.adapter.data.remove(text)
					self.tech_list_view._trigger_reset_populate()
				except requests.exceptions.ConnectionError:
					message = 'Check your internet connetcion'
					popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
					popup.open()



	def show_selected_value_spinner(self,spinner, text):
		self.selected_device=text
		self.getDevices()

	def my_list_functionalities(self,ad):
		'''if self.mode == 0:
			try:
				global textofDeviceStudent,devices_names, deviceID
				textofDeviceStudent=str(ad.selection[0].text)+str(devices_names[self.selected_device])
				deviceID = int(textofDeviceStudent[4:12])
				self.manager.current = 'clear_screen'
				self.manager.current = 'device_tech_screen'
				
			except:
				pass'''
		if self.mode == 1:
			if ad.selection:
				print ("imahere")
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
			strpre="ID: {}\nType: {}\nlocation: {}\nstate: {}\nrate: {}"
			#self.tech_list_view.adapter.bind(on_selection_change=self.my_list_functionalities)
			for s in data:
				try:
					self.tech_list_view.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],s[4]/s[5])])
				except:
					self.tech_list_view.adapter.data.extend([strpre.format(s[0],s[1],s[2],s[3],'Not Rated')])
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
				self.tech_list_view.adapter.data.extend(['sID: {}\ndID: {}\nST: {}\nET: {}\nReserved: {}\nIn Use: {}'.format(item[0], item[1], item[2][:19], item[3][:19], item[4], item[5])])
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

class PCOthersScreen(Screen):
	def on_pre_enter (self):
		try:
			self.pcs = requests.get('http://warehub-api.azurewebsites.net/retrive_devices/5')
			self.pcs = json.loads(self.pcs.text)
			self.soft = requests.get('http://warehub-api.azurewebsites.net/getsoftware')
			self.soft = json.loads(self.soft.text)
			self.OSs = requests.get('http://warehub-api.azurewebsites.net/getOS')
			self.OSs = json.loads(self.OSs.text)

		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			self.manager.current = 'tech_screen'
		self.ids.PC_Labelspinner.values=[str(int(x[0])%1000000) for x in self.pcs]
		self.ids.Software_sppiner.values=[x[1] for x in self.soft ]
		self.ids.OS_sppiner.values=[x[1] for x in self.OSs ]

	def addtoPC(self):
		if self.ids.PC_Labelspinner.text=='PC Label':
			message = 'Choose the Device first'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return

		if self.ids.Software_sppiner.text != 'Software':
			dtype = [x[0] for x in self.soft if x[1]==self.ids.Software_sppiner.text]
			payload = {'pc_id': [int(self.ids.PC_Labelspinner.text)+50000000],'software_id':[dtype[0]]}
			try:
				isLoggedin = requests.post('http://warehub-api.azurewebsites.net/add_pc_software', data = payload)
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
				return

		if self.ids.OS_sppiner.text != 'OS':
			dtype = [x[0] for x in self.OSs if x[1]==self.ids.OS_sppiner.text]
			payload = {'pc_id': [int(self.ids.PC_Labelspinner.text)+50000000],'os_id':[dtype[0]]}
			try:
				isLoggedin = requests.post('http://warehub-api.azurewebsites.net/add_pc_os', data = payload)
			except requests.exceptions.ConnectionError:
				message = 'Check your internet connetcion'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
				return
		message = 'Done !'
		popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
		popup.open()



class ClearScreen(Screen):
	pass


class SaveScreen(Screen):
	def on_pre_enter(self):
		self.ids.my_box.add_widget(Button(text = 'Save Information', size_hint = (0.3, 0.3), on_release = self.back))

	def back(self, o):
		self.ids.my_box.clear_widgets()
		if myType == 0:
			self.manager.current = 'clear_screen'
			self.manager.current = 'manager_screen'
		elif myType == 1:
			self.manager.current = 'clear_screen'
			self.manager.current = 'student_screen'
		else:
			self.manager.current = 'clear_screen'
			self.manager.current = 'tech_screen'



class AddDeviceScreen(Screen):
	def show_selected_value_spinner(self,spinner,text):
		for onetext in self.texts:
			onetext.opacity=0
		global devices_names
		self.device_id = devices_names[text]
		if (self.device_id=='5'):
			self.texts[0].opacity=1
			self.texts[1].opacity=1
			self.texts[2].opacity=1
		elif (self.device_id=='7'):
			self.texts[3].opacity=1
	
	def show_spinner_state(self,spinner,text):
		self.state=text
	def show_spinner_location(self,spinner,text):
		self.location=text        		
	def on_pre_enter (self):
		self.device_id =0
		self.state=10
		self.location=10
		self.texts=[self.ids.RAM_addDev_text,self.ids.GPU_addDev_text,self.ids.CPU_addDev_text,self.ids.Code_addDev_text]
		self.ids.type_spinner.bind(text=self.show_selected_value_spinner)
		self.ids.state_sppiner.bind(text=self.show_spinner_state)
		self.ids.location_sppiner.bind(text=self.show_spinner_location)
		

	def adddevice(self):
    	#self.manager.current = 'student_screen'
		if (self.device_id==0):
			message = 'Please chooes device type'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return
		if(self.state ==10):
			message = 'Please choose device state'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return
		
		if(self.location==10):
			message = 'Please choose device location'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return

		if(len(self.ids.label_addDev_text.text) ==0 or len(self.ids.dtype_addDev_text.text) ==0):
			message = 'Please enter device data'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()
			return
		for test in self.texts:
			if(test.opacity==1 and len(test.text) ==0):
				message = 'Please enter device data'
				popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
				popup.open()
				return


		try:
			self.device_id=int(self.device_id)
			id = self.device_id * 10000000 + int(self.ids.label_addDev_text.text)
			dtype = self.ids.dtype_addDev_text.text
			if (self.device_id==5):
				payload = {'id': [str(id)],'dtype':[dtype],'location':[self.location],'state':[self.state],'OVERALL_REVIEW':['0'],'NUM_REVIEWS':['0'],'tech_id':[str(ID)],'CPU':[self.ids.CPU_addDev_text.text],'GPU':[self.ids.GPU_addDev_text.text],'RAM':[self.ids.RAM_addDev_text.text]}
			elif (self.device_id==7):
				payload = {'id': [str(id)],'dtype':[dtype],'location':[self.location],'state':[self.state],'OVERALL_REVIEW':['0'],'NUM_REVIEWS':['0'],'tech_id':[str(ID)],'code':[self.texts[3].text]}
			else:
				payload = {'id': [str(id)],'dtype':[dtype],'location':[self.location],'state':[self.state],'OVERALL_REVIEW':['0'],'NUM_REVIEWS':['0'],'tech_id':[str(ID)]}

			isLoggedin = requests.post('http://warehub-api.azurewebsites.net/add_device', data = payload)
			message = 'Done !'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

			#t.add_device(int(result['id'][0]), result['dtype'][0], int(result['location'][0]), result['state'][0], result['OVERALL_REVIEW'][0],result['NUM_REVIEWS'][0],result['tech_id'][0],result['CPU'][0],result['GPU'][0],result['RAM'][0])

		except ValueError:
			message = 'invalid data'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()

		except requests.exceptions.ConnectionError:
			message = 'Check your internet connetcion'
			popup = Popup(title='', content=Label(text=message), size_hint=(None, None), size = (500, 200))
			popup.open()




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
