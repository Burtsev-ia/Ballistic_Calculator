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
        self.output_label_horizontal = Label()
        layout.add_widget(self.output_label_horizontal)
        self.btn = Button(text="Вычислить", on_press=self.calculate)
        layout.add_widget(self.btn)

        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t1 = TextInput(hint_text='Расстояние по горизонтали(М)', input_filter='float', multiline=False)
        layout.add_widget(self.t1)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t5 = TextInput(hint_text='перепад высоты (М)', input_filter='float', multiline=False)
        layout.add_widget(self.t5)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t2 = TextInput(hint_text='Калибр снаряда(ММ)', input_filter='float', multiline=False)
        layout.add_widget(self.t2)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t3 = TextInput(hint_text='Масса снаряда(КГ)', input_filter='float', multiline=False)
        layout.add_widget(self.t3)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t4 = TextInput(hint_text='Начальная скорость(м/с)', input_filter='float', multiline=False)
        layout.add_widget(self.t4)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t6 = TextInput(hint_text='скорость ветра(м/с)', input_filter='float', multiline=False)
        layout.add_widget(self.t6)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t7 = TextInput(hint_text='угол ветра(°) {{встречный-0°, справа-90°, сзади-180°, слева-270°}}', input_filter='float', multiline=False)
        layout.add_widget(self.t7)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)

        self.t8 = TextInput(hint_text='коэфф сопротивления',
                            input_filter='float', multiline=False)
        layout.add_widget(self.t8)

        sep = Widget(size_hint_y=None, height=30)
        layout.add_widget(sep)
        return layout

    def calculate(self, instance):
        try:
            self.a = float(self.t4.text)
            self.d = float(self.t2.text)
            self.x = float(self.t1.text)
            self.m = float(self.t3.text)
            self.y = float(self.t5.text)
            self.veter = float(self.t6.text)
            self.ugol_vetra = float(self.t7.text)
            self.koeff = float(self.t8.text)


            g = 9.806552

            Cr = self.koeff  # лобовой кэф сопротивления
            Sm = math.pi * math.pow(self.d / 1000, 2) / 4  # площадь
            plv = 1.225  # плотность воздуха
            Kr = Cr * Sm * plv / 2  # коэф сопротивления
            dt = 0.01  # шаг
            w = self.veter # общая скорость ветра
            beta = self.ugol_vetra / 180 * math.pi # угол ветра в радианах
            wx = -math.cos(beta) * w # считаем что при нуле градусов дует в лоб
            wz = -math.sin(beta)* w # ось z направлена вправо
            # print(wx, wz)
            # print(wx)
            kz = 0.5
            z = 0 # расстояние по оси z на которое тело сместит ветер


            tetamin = 45 / 180 * math.pi
            tetamax = 90 / 180 * math.pi
            tetasr = (tetamax + tetamin) / 2
            vx1 = self.a * math.cos(tetasr) #ачальная скорость относительно земли

            def error(tetasr):
                vx1 = self.a * math.cos(tetasr) + wx # начальная скорость относительно воздуха
                vy1 = self.a * math.sin(tetasr)
                y1 = 0
                x1 = 0
                t = 0  # время полета
                ymax = 0
                parametr = 0  # доп параметр чтобы понять что цель прошла верхнюю точку
                while 1:
                    v = (vx1 ** 2 + vy1 ** 2) ** 0.5
                    ax = -(Kr / self.m) * v * vx1
                    ay = -g - (Kr / self.m) * v * vy1
                    vx2 = vx1 + ax * dt
                    vy2 = vy1 + ay * dt
                    x2 = x1 + (vx1 - wx) * dt # отнимаем wx т.к считаем перемещение относительно земли
                    y2 = y1 + vy1 * dt
                    t += dt
                    ymax = max(ymax, y2)
                    # print(x2, y2)
                    if y2 >= self.y:
                        param = 1
                    if y2 <= self.y and param == 1:
                        delta = self.x - x2
                        # print(ymax)
                        return delta, t, x2

                        break

                    x1 = x2
                    y1 = y2
                    vx1 = vx2
                    vy1 = vy2


            e = error(tetasr)
            co = 0 # количество бинарных поисков
            while abs(e[0]) >= 0.01:  # пока погрешность больше 1см
                co += 1
                if error(tetasr)[0] > 0:
                    tetamax = tetasr
                else:
                    tetamin = tetasr
                tetasr = (tetamin + tetamax) / 2
                e = error(tetasr)
                # print(e)
                if co > 20:
                    self.output_label.text = "Выстрел невозможен"
                    break



            T = e[1] # время полета
            z = wz * T * kz
            popravka_z = math.atan(-z/self.x) * 180 / math.pi # поправка угла вдоль оси z
            if co > 20:
                self.output_label.text = "Выстрел невозможен"
                self.output_label_horizontal.text = ""
            else:

                tetasr = tetasr * 180 / math.pi

                degrees = tetasr
                minutes = (degrees - int(degrees)) * 60
                seconds = (minutes - int(minutes)) * 60
                # print(int(degrees), int(minutes), int(seconds),tetasr)

                self.output_label.text = f"Угол по вертикали: {int(degrees)}° {int(minutes)}' {int(seconds)}''"
                self.output_label_horizontal.text = "Угол по горизонтали(°) : {:.3f}".format(popravka_z)
            '''else:
                self.output_label.text = "Угол по вертикали(°) : {:.3f}".format(tetasr*180/math.pi)
                self.output_label_horizontal.text = "Угол по горизонтали(°) : {:.3f}".format(popravka_z)
                # print(popravka_z)
                '''



        except ValueError:
            self.output_label.text = "Введите данные корректно"


if __name__ == '__main__':
    MyApp().run()