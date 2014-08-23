import kivy
kivy.require('1.8.0')

import waterCosts
import database_functions

from math import pi
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown

class UserInput(FloatLayout):
    def __init__(self,**kwargs):
        super(UserInput,self).__init__(**kwargs)
        self.city = 'Austin'
        print self.city

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
        popup = Popup(title='Where do you live?',content=content, auto_dismiss = False, on_dismiss = lambda x: self.changeCity(content.getCity()))
        content.ids.closeSettingsButton.bind(on_press=popup.dismiss)
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
            buttonText = database_functions.match_by_name(self.ids.plantName.text)
            self.dropdown = PlantNameDropdown(buttonText)
            self.dropdown.open(self.ids.plantName)
            self.dropdown.bind(on_select=lambda instance,x: self.selectPlant(x)) #setattr(self.ids.plantName, 'text', x))

    def selectPlant(self,text):
        '''This is a dummy function: it does not do anything useful yet!'''
        self.ids.plantName.text = text
        # need to change water needed, size, etc. based on plant choice...

class cityChoice(FloatLayout):
    def getCity(self):
        if self.ids.cityAustin.state=='down':
            return 'Austin'
        elif self.ids.cityHouston.state=='down':
            return 'Houston'
        elif self.ids.cityDallas.state=='down':
            return 'Dallas'
        elif self.ids.citySanAntonio.state=='down':
            return 'San Antonio'

class PlantNameDropdown(DropDown):
    def __init__(self,textList):
        super(PlantNameDropdown,self).__init__()
        self.selected=''
        for t in textList:
            # The button height needs to be set or kivy gets really confused!
            b=Button(text=t, size_hint_y=None, height=44)
            b.bind(on_release=lambda b: self.select(b.text))
            self.add_widget(b)

class PlantApp(App):
    def build(self):
        return UserInput()


if __name__ == '__main__':
    PlantApp().run()
