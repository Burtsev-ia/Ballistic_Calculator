from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
import math


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.output_label = Label(text="поле ответа", outline_color=(0.6, 0.9, 0.9, 1))
        layout.add_widget(self.output_label)

        self.btn = Button(text="Calculate", on_press=self.calculate)
        layout.add_widget(self.btn)

        sep1 = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep1)

        self.text_input1 = TextInput(hint_text='Расстояние по горизонтали(М)', input_filter='float', multiline=False)
        layout.add_widget(self.text_input1)

        sep2 = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep2)

        self.text_input2 = TextInput(hint_text='Перепад высоты(М)', input_filter='float', multiline=False)
        layout.add_widget(self.text_input2)

        sep3 = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep3)

        self.text_input3 = TextInput(hint_text='Начальная скорость(м/с)', input_filter='float', multiline=False)
        layout.add_widget(self.text_input3)



        return layout

    def calculate(self, instance):
        try:
            self.a = float(self.text_input1.text)
            self.b = float(self.text_input2.text)
            self.x = float(self.text_input3.text)
            g = 9.806552


            c = ((self.x ** 2) / (g * self.a)) \
                * (1 + (( self.x**4\
                          - 2 * g *self.b * self.x **2 \
                         - g ** 2 * self.a **2) ** 0.5) / self.x **2)

            if self.x < (g*(self.b +(self.a**2+self.b**2)**0.5))**0.5 :
                self.output_label.text = "выстрел невозможен"
            else:
                c=math.degrees(math.atan(c))
                self.output_label.text = "Угол(°) : {}".format(c)
        except ValueError:
            self.output_label.text = "Введите данные корректно"


if __name__ == '__main__':
    MyApp().run()
