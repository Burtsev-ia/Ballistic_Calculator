from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
import math


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.output_label = Label(text="поле ответа")
        layout.add_widget(self.output_label)
        self.btn = Button(text="Вычислить", on_press=self.calculate)
        layout.add_widget(self.btn)

        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t1 = TextInput(hint_text='Расстояние по горизонтали(М)', input_filter='float', multiline=False)
        layout.add_widget(self.t1)

        sep = Widget(size_hint_y=None, height=40)
        layout.add_widget(sep)

        self.t5 = TextInput(hint_text='перепад высоты (М)', input_filter='float', multiline=False)
        layout.add_widget(self.t5)

        sep = Widget(size_hint_y=None, height=40)
        layout.add_widget(sep)

        self.t2 = TextInput(hint_text='Калибр снаряда(ММ)', input_filter='float', multiline=False)
        layout.add_widget(self.t2)

        sep = Widget(size_hint_y=None, height=40)
        layout.add_widget(sep)

        self.t3 = TextInput(hint_text='Масса снаряда(КГ)', input_filter='float', multiline=False)
        layout.add_widget(self.t3)

        sep = Widget(size_hint_y=None, height=40)
        layout.add_widget(sep)

        self.t4 = TextInput(hint_text='Начальная скорость(м/с)', input_filter='float', multiline=False)
        layout.add_widget(self.t4)

        sep = Widget(size_hint_y=None, height=40)
        layout.add_widget(sep)
        return layout

    def calculate(self, instance):
        try:
            self.a = float(self.t4.text)
            self.d = float(self.t2.text)
            self.x = float(self.t1.text)
            self.m = float(self.t3.text)
            self.y = float(self.t5.text)

            g = 9.806552

            Cr = 0.22  # лобовой кэф сопротивления
            Sm = math.pi * math.pow(self.d / 1000, 2) / 4  # площадь
            plv = 1.225  # плотность воздуха
            Kr = Cr * Sm * plv / 2  # коэф сопротивления
            dt = 0.01  # шаг
            xx = []
            yy = []
            tt = []
            uu = []
            vv = []

            tetamin = 45 / 180 * math.pi
            tetamax = 90 / 180 * math.pi
            tetasr = (tetamax + tetamin) / 2
            vx1 = self.a * math.cos(tetasr)

            def error(tetasr):
                vx1 = self.a * math.cos(tetasr)
                vy1 = self.a * math.sin(tetasr)
                y1 = 0
                x1 = 0
                parametr = 0  # доп параметр чтобы понять что цель прошла верхнюю точку
                while 1:
                    v = (vx1 ** 2 + vy1 ** 2) ** 0.5
                    ax = -(Kr / self.m) * v * vx1
                    ay = -g - (Kr / self.m) * v * vy1
                    vx2 = vx1 + ax * dt
                    vy2 = vy1 + ay * dt
                    x2 = x1 + vx1 * dt
                    y2 = y1 + vy1 * dt
                    # print(x2, y2)
                    if y2 >= self.y:
                        param = 1
                    if y2 <= self.y and param == 1:
                        delta = self.x - x2
                        return delta
                        break

                    x1 = x2
                    y1 = y2
                    vx1 = vx2
                    vy1 = vy2


            e = error(tetasr)
            co = 0 # количество бинарных поисков
            while abs(e) >= 0.01:  # пока погрешность больше 1см
                co += 1
                if error(tetasr) > 0:
                    tetamax = tetasr
                else:
                    tetamin = tetasr
                tetasr = (tetamin + tetamax) / 2
                e = error(tetasr)
                # print(e)
                if co > 20:
                    self.output_label.text = "Выстрел невозможен"
                    break

            if co > 20:
                self.output_label.text = "Выстрел невозможен"
            else:
                tetasr = tetasr * 180 / math.pi
                degrees = tetasr
                minutes = (degrees - int(degrees)) * 60
                seconds = (minutes - int(minutes)) * 60
                print(int(degrees), int(minutes), int(seconds),tetasr)

                self.output_label.text = f"{int(degrees)}° {int(minutes)}' {int(seconds)}''"


        except ValueError:
            self.output_label.text = "Введите данные корректно"


if __name__ == '__main__':
    MyApp().run()