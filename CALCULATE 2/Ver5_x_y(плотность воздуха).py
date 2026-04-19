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
            plotnosti = {
                0: 1.22500,
                100: 1.21326,
                200: 1.20164,
                300: 1.19014,
                400: 1.17877,
                500: 1.16752,
                600: 1.15638,
                700: 1.14536,
                800: 1.13445,
                900: 1.12366,
                1000: 1.11298,
                1100: 1.10240,
                1200: 1.09194,
                1300: 1.08159,
                1400: 1.07134,
                1500: 1.06120,
                1600: 1.05116,
                1700: 1.04122,
                1800: 1.03139,
                1900: 1.02166,
                2000: 1.01203,
                2100: 1.00249,
                2200: 0.99305,
                2300: 0.98371,
                2400: 0.97446,
                2500: 0.96530,
                2600: 0.95623,
                2700: 0.94726,
                2800: 0.93837,
                2900: 0.92957,
                3000: 0.92086,
                3100: 0.91223,
                3200: 0.90369,
                3300: 0.89523,
                3400: 0.88686,
                3500: 0.87856,
                3600: 0.87035,
                3700: 0.86222,
                3800: 0.85417,
                3900: 0.84619,
                4000: 0.83830,
                4100: 0.83048,
                4200: 0.82273,
                4300: 0.81506,
                4400: 0.80747,
                4500: 0.79994,
                4600: 0.79249,
                4700: 0.78511,
                4800: 0.77780,
                4900: 0.77056,
                5000: 0.76339,
                5100: 0.75629,
                5200: 0.74926,
                5300: 0.74230,
                5400: 0.73541,
                5500: 0.72859,
                5600: 0.72183,
                5700: 0.71513,
                5800: 0.70850,
                5900: 0.70193,
                6000: 0.69543,
                6100: 0.68899,
                6200: 0.68261,
                6300: 0.67629,
                6400: 0.67003,
                6500: 0.66383,
                6600: 0.65769,
                6700: 0.65161,
                6800: 0.64559,
                6900: 0.63962,
                7000: 0.63371,
                7100: 0.62786,
                7200: 0.62206,
                7300: 0.61631,
                7400: 0.61062,
                7500: 0.60498,
                7600: 0.59940,
                7700: 0.59386,
                7800: 0.58838,
                7900: 0.58295,
                8000: 0.57757,
                8100: 0.57223,
                8200: 0.56695,
                8300: 0.56171,
                8400: 0.55652,
                8500: 0.55138,
                8600: 0.54628,
                8700: 0.54123,
                8800: 0.53622,
                8900: 0.53126,
                9000: 0.52635,
                9100: 0.52147,
                9200: 0.51664,
                9300: 0.51186,
                9400: 0.50711,
                9500: 0.50241,
                9600: 0.49775,
                9700: 0.49313,
                9800: 0.48855,
                9900: 0.48401,
                10000: 0.47951
            } # таблица плотностей воздуха от высоты


            g = 9.806552

            Cr = self.koeff  # лобовой кэф сопротивления
            Sm = math.pi * math.pow(self.d / 1000, 2) / 4  # площадь
            plv1 = 1.225  # плотность воздуха начальная
            Kr1 = Cr * Sm * plv1 / 2  # коэф сопротивления
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

            def plotnost_pick(y1):
                if y1 >= 10000:
                    return (plotnosti[5000])
                if y1 <= 0:
                    return (plotnosti[0])
                for i in plotnosti:
                    if i - 100 <= y1 and i + 100 > y1:
                        return (plotnosti[i])

            def error(tetasr):
                vx1 = self.a * math.cos(tetasr) + wx # начальная скорость относительно воздуха
                vy1 = self.a * math.sin(tetasr)
                y1 = 0
                x1 = 0
                t = 0  # время полета
                ymax = 0
                parametr = 0  # доп параметр чтобы понять что цель прошла верхнюю точку
                ypred = 0 # доп переменная для оптимизации
                while 1:
                    plv = plv1
                    Kr = Kr1
                    if abs(ypred - y1) >= 100: # немного оптимизировать чтобы не считать каждый раз плотность
                        plv = plotnost_pick(y1)
                        Kr = Cr * Sm * plv / 2
                        ypred = y1

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