from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.button import Button
import math









class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.output_label = Label(text="поле ответа" )
        layout.add_widget(self.output_label)
        self.btn = Button(text="Вычислить", on_press=self.calculate)
        layout.add_widget(self.btn)

        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t1 = TextInput(hint_text='Расстояние по горизонтали(М)', input_filter='float', multiline=False)
        layout.add_widget(self.t1)

        sep= Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t2 = TextInput(hint_text='Калибр снаряда(ММ)', input_filter='float', multiline=False)
        layout.add_widget(self.t2)

        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t3 = TextInput(hint_text='Масса снаряда(КГ)', input_filter='float', multiline=False)
        layout.add_widget(self.t3)


        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)

        self.t4 = TextInput(hint_text='Начальная скорость(м/с)', input_filter='float', multiline=False)
        layout.add_widget(self.t4)

        sep = Widget(size_hint_y=None, height=50)
        layout.add_widget(sep)



        return layout
    def calculate(self, instance):
        try:
            self.a = float(self.t4.text)
            self.d = float(self.t2.text)
            self.x = float(self.t1.text)
            self.m = float(self.t3.text)
            g = 9.806552

            Cr = 0.22
            Sm=math.pi * math.pow(self.d/1000,2) / 4 #площадь
            plv=1.225
            Kr=Cr*Sm*plv/(2*self.m)
            dt=0.01
            xx=[]
            yy=[]
            tt=[]
            uu=[]
            vv=[]
            for teta_gr in range(0,46):
                teta1 = math.pi * (teta_gr+45) / 180.
                v1, x1, y1, t = self.a, 0, 0, 0
                while(1):

                    v2=v1-dt*(Kr*math.pow(v1,2)+g*math.sin(teta1))
                    teta2=teta1-dt*g*math.cos(teta1)/v1
                    x2=x1+(v1*math.cos(teta1))*dt
                    y2=y1+(v1*math.sin(teta1))*dt
                    t=t+dt


                    #Достигли уровня падения (условно земля, уровень 0, поставить например -1 если стреляете сверху на метр)
                    if y2<=0:

                        xx.append(x2)
                        tt.append(t)
                        vv.append(v2)
                        uu.append(teta_gr+45)
                        break
                    v1=v2
                    teta1=teta2
                    x1=x2
                    y1=y2
            for i in range(len(xx)-2) :
                if xx[i]>self.x and xx[i+2]<self.x :
                    tetra_gr=(uu[i+1])

                    break
                else :
                    tetra_gr=-1

            if tetra_gr!=-1 :

                xx1=[]
                vv1=[]
                tt1=[]
                uu1=[]



                for i in range((tetra_gr ) * 100, (tetra_gr+1) * 100):
                    teta1 = math.pi * (i/100) / 180.
                    v1, x1, y1, t = self.a, 0, 0, 0
                    while (1):

                        v2 = v1 - dt * (Kr * math.pow(v1,2) + g * math.sin(teta1))
                        teta2 = teta1 - dt * g * math.cos(teta1) / v1
                        x2 = x1 + (v1 * math.cos(teta1)) * dt
                        y2 = y1 + (v1 * math.sin(teta1)) * dt
                        t = t + dt
                        # Достигли уровня падения (условно земля, уровень 0, поставить например -1 если стреляете сверху на метр)
                        if y2 <= 0:

                            xx1.append(x2)
                            tt1.append(t)
                            vv1.append(v2)
                            uu1.append(i/100)
                            break
                        v1 = v2
                        teta1 = teta2
                        x1 = x2
                        y1 = y2
                for i in range(len(uu1)-2) :
                    if xx1[i]>self.x and xx1[i+2]<self.x :
                        self.output_label.text = "Угол(°) : {}".format(uu1[i+1])
            else :
                self.output_label.text = "Выстрел невозможен"

        except ValueError:
                self.output_label.text = "Введите данные корректно"
if __name__ == '__main__':
    MyApp().run()