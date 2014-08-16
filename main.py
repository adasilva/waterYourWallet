import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class UserInput(FloatLayout):
    pass

class PlantApp(App):
    def build(self):
        return UserInput()


if __name__ == '__main__':
    PlantApp().run()
