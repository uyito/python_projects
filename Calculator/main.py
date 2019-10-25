import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

class MyFirstWidget(BoxLayout):

    def text(self, val):
        print('text input text is: {txt}'.format(txt=val))

class CalculatorGridLayout(GridLayout):

    def calculate(self, calculation):
        if calculation:
            try:
                self.display.text = str(eval(calculation))
            except:
                self.display.text = "Error"

class CalcApp(App):

    def build(self):
        return MyFirstWidget()
            # , CalculatorGridLayout()






# calcApp = CalcApp()
# calcApp.run()
CalcApp().run()


