import kivy
kivy.require('1.8.0')

from math import pi
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class UserInput(FloatLayout):
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

            # Average person uses 100 gallons of water per day
            # (http://www.epa.gov/WaterSense/pubs/indoor.html; accessed Aug 2014)
            # Cost of water from City of Austin utilities depends on total usage
            # The average household (family of 4) uses 12,000 gallons per month
            # Austin charges $9.95 per 1000 gallons for 11,001 - 20,000 total
            # gallons of usage
            # (http://www.austintexas.gov/department/austin-water-utility-service-rates; accessed Aug 2014)

            # Cost per gallon:
            cpg = 9.95/1000.

            # Total cost
            cost = cpg*volH2O*4 # multiply by 4 to get monthly cost

            self.ids.result.text='$ %0.2f per month' %(cost,)

        except:
            if spread==None:
                self.ids.result.text='Make sure the plant size was chosen.'
            else:
                self.ids.result.text='Enter a number in water required text box.'
        return None

    def changeCity(self,city):
        self.ids.cityLabel.text = 'City:   %s, TX' %(city,)
        return None
        
    def settingsPopup(self):
        content = cityChoice()
        popup = Popup(title='Where do you live?',content=content, auto_dismiss = False, on_dismiss = lambda x: self.changeCity(content.getCity()))
        content.ids.closeSettingsButton.bind(on_press=popup.dismiss)
        popup.open()
        return None
        
    def helpPopup(self):
        content = helpLayout()
        popup = Popup(title='Help with Water Your Wallet', 
                      content=content, auto_dismiss=True)
        popup.open()
        return None
        
class helpLayout(FloatLayout):
    pass

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

class PlantApp(App):
    def build(self):
        return UserInput()


if __name__ == '__main__':
    PlantApp().run()
