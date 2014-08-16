import kivy
kivy.require('1.8.0')

from math import pi
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget



class UserInput(FloatLayout):
    def calculateWaterCost(self,inches=1,number=1,size='small'):
        '''calculates the cost per month of water for a plant, name.

    Inputs: 
    name - name of plant
    inches - inches per week required
    number - number of this type of plant
    size - size of plant (small, medium, or large)
    '''
        # determine spread (in inches) of plant based on size
        if size=='small':
            spread = 12
        elif size=='medium':
            spread = 24
        else:
            spread = 48        

        # volume of water is the inches times the spread
        volH2O = pi*(spread/2)**2*inches
        # convert to gallons (from google)
        volH2O = volH2O*0.004329

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

        self.ids.result.text='$'+str(cost)
        return None


class PlantApp(App):
    def build(self):
        return UserInput()


if __name__ == '__main__':
    PlantApp().run()
