import kivy
kivy.require('1.8.0')

import waterCosts
from database_functions import plantdb

from math import pi
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.config import ConfigParser
from kivy.uix.settings import Settings

class LoginScreen(Screen):
    def __init__(self,config,**kwargs):
        super(LoginScreen,self).__init__(**kwargs)
        self.config = config

    def save(self):
        username = self.ids.username.text
        password = self.ids.password.text
        self.config.set('remotedb','username',username)
        self.config.set('remotedb','password',password)
        self.manager.current = 'main'


class UserInput(Screen):
    def __init__(self,config,**kwargs):
        super(UserInput,self).__init__(**kwargs)
        self.city = 'Austin'
        self.config = config

    def startdb(self,*args,**kwargs):
        try:
            self.db = plantdb(self.config.get('remotedb','username'),self.config.get('remotedb','password'),self.config.get('remotedb','host'),self.config.get('remotedb','replica set'))
            self.ids.warningMessage.text = ''

        except:
            self.db = None 
            self.ids.warningMessage.text = '[color=993333][ref=warn]Could not connect to database.[/ref][/color]'
            popupmsg = 'Could not connect to database.\nCheck your username and password. If you cannot connect, you may still use the app by entering the information by hand!'
            content = helpLayout(popupmsg)
            popup = Popup(title='Help with Water Your Wallet', 
                      content=content, auto_dismiss=True,
                      size_hint=(0.75,0.9))
            self.ids.warningMessage.on_ref_press = popup.open

        return None

    def closedb(self,*args,**kwargs):
        if self.db != None:
            self.db.conn.close()

    def calculateWaterCost(self):
        '''calculates the cost per month of water for a plant.

    Inputs are obtained from user input:
    name - name of plant
    inches - inches per week required
    numplants - number of this type of plant
    size - size of plant (small, medium, or large, chosen via toggle button)
    '''
        # determine spread (in inches) of plant based on size
        numplants=int(self.ids.numPlants.value)
        if self.ids.plantSmall.state=='down':
            spread = 12
        elif self.ids.plantMedium.state=='down':
            spread = 24
        elif self.ids.plantLarge.state=='down':
            spread = 48
        else:
            spread = None
        try:
            inches = float(self.ids.waterSlider.value)
            # volume of water is the inches times the spread
            volH2O = pi*(spread/2)**2*inches
            # convert to gallons (from google) and multiply by number of plants
            volH2O = volH2O*0.004329*numplants

            allCosts = waterCosts.waterCosts()
            if self.city == 'Austin':
                cpg = allCosts.austin
            elif self.city == 'San Antonio':
                cpg = allCosts.sanAntonio
            elif self.city == 'Dallas':
                cpg = allCosts.dallas
            elif self.city == 'Houston':
                cpg = allCosts.houston
            else:
                cpg = None

            # Total cost
            cost = cpg*volH2O*4 # multiply by 4 to get monthly cost

            self.ids.result.text='$ %0.2f per month' %(cost,)

        except:
            if spread==None:
                self.ids.result.text='Make sure the plant size was chosen.'
            elif cpg==None:
                self.ids.result.text='Did not receive city choice.'
            else:
                self.ids.result.text='Enter a number in water required text box.'
        return None

    def changeCity(self,city):
        self.city = city
        self.ids.cityLabel.text = 'City:   %s, TX' %(city,)
        return None
        
    def settingsPopup(self):
        content = cityChoice()
        popup = Popup(title='Where do you live?',
                      content=content, auto_dismiss = True, 
                      on_dismiss = lambda x: self.changeCity(content.getCity()),
                      size_hint=(0.75,0.9))
        popup.open()
        return None
        
    def helpPopup(self,text):
        content = helpLayout(text)
        popup = Popup(title='Help with Water Your Wallet', 
                      content=content, auto_dismiss=True,
                      size_hint=(0.75,0.9))
        popup.open()
        return None
        
    def openPlantNameDropdown(self):
        try:
            self.dropdown.dismiss()  #dismiss if already exists
        except:
            pass
        if self.ids.plantName.text=='':
            pass  # wait for input text
        else:
            try:
                buttonText = self.db.match_by_name(self.ids.plantName.text)
                self.dropdown = PlantNameDropdown(buttonText)
                self.dropdown.open(self.ids.plantName)
                self.dropdown.bind(on_select=lambda instance,x: self.selectPlant(x)) #setattr(self.ids.plantName, 'text', x))
            except:
                pass

    def selectPlant(self,text):
        '''When the plant is selected, the data is taken from database and used to set the size toggle button and water slider bars.'''
        self.ids.plantName.text = text
        try:
            properties = self.db.get_properties_by_name(text)
        except:
            properties = {'span':0, 'water':0}
        self.ids.waterSlider.value = properties['water']
        if properties['span']<=12:
            self.ids.plantMedium.state = 'normal'
            self.ids.plantLarge.state = 'normal'
            self.ids.plantSmall.state = 'down'
        elif properties['span']<=24:
            self.ids.plantSmall.state = 'normal'
            self.ids.plantLarge.state = 'normal'
            self.ids.plantMedium.state = 'down'
        elif properties['span']>24:
            self.ids.plantSmall.state = 'normal'
            self.ids.plantMedium.state = 'normal'
            self.ids.plantLarge.state = 'down'
        else:
            self.ids.plantSmall.state = 'normal'
            self.ids.plantMedium.state = 'normal'
            self.ids.plantLarge.state = 'normal'

class cityChoice(GridLayout):
    def getCity(self):
        if self.ids.cityAustin.state=='down':
            return 'Austin'
        elif self.ids.cityHouston.state=='down':
            return 'Houston'
        elif self.ids.cityDallas.state=='down':
            return 'Dallas'
        elif self.ids.citySanAntonio.state=='down':
            return 'San Antonio'

class helpLayout(FloatLayout):
    def __init__(self,text,**kwargs):
        super(helpLayout,self).__init__(**kwargs)
        self.ids.helpText.text=text


class loginLayout(GridLayout):
    def __init__(self,**kwargs):
        super(loginLayout,self).__init__(**kwargs)
        

class PlantNameDropdown(DropDown):
    def __init__(self,textList):
        super(PlantNameDropdown,self).__init__()
        self.selected=''
        for t in textList:
            # The button height needs to be set or kivy gets really confused!
            b=Button(text=t, size_hint_y=None, height=44)
            b.bind(on_release=lambda b: self.select(b.text))
            self.add_widget(b)


class AppScreenManager(ScreenManager):
    pass

class PlantApp(App):
    def build_config(self, config):
        config.setdefaults('remotedb', 
                           {'host': '',
                            'replica set': '',
                            'username': '', 'password':''})

    def build(self):
        sm = AppScreenManager()

        config = ConfigParser()
        config.read('plant.ini')

        screen1 = UserInput(config, name='main')
        screen1.bind(on_enter = screen1.startdb)
        screen1.bind(on_leave = screen1.closedb)
        sm.add_widget(screen1)

        sm.add_widget(LoginScreen(config, name='login'))
        return sm


if __name__ == '__main__':
    PlantApp().run()
