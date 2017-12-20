from backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import requests

data = requests.get('http://warehub-api.azurewebsites.net/getcrowded_day')
data = json.loads(data.text)
date = []
dss = []

for s in data:
    date.append(s[0])
    dss.append(s[1])

fig, ax = plt.subplots()

ax.plot( date,dss)
ax.set_title('Most Days of Demands')

ax.set_xlabel('Days')
ax.set_ylabel('Number of Demands')
ax.set_xticklabels([])


ax.set_ylim(0, max(dss)+5)

ax.grid(True)

fig.autofmt_xdate()


class MyApp(App):

    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box

MyApp().run()
