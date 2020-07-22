from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '600')

import kivy
from kivy.app import App
from kivymd.app import MDApp
from os.path import dirname
import playmo as pl
import playimg as plimg
import playword as plword
from playword import *

import time
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty,NumericProperty,ListProperty
from kivy.uix.actionbar import ActionBar , ActionItem, ActionView, ActionPrevious, ActionGroup, ActionButton
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
#키비폰트 정하기
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('c:/windows/fonts')
LabelBase.register(DEFAULT_FONT, 'H2GTRE.TTF')
from kivy.lang import Builder
with open(f"{dirname(__file__)}/switch.kv", 'rt', encoding='utf-8') as f: # Note the name of the .kv 
    Builder.load_string(f.read())

from kivy.uix.button import Button 
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
import pandas as pd
##맷립 임포트
import matplotlib
matplotlib.use(r'module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt

#비디오목록
import playmo
from kivy.uix.videoplayer import VideoPlayer
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
import os
from kivy.uix.recycleview import RecycleView

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label


global path_real
path_real='asdkjfsdkjfkl'

global path_real2
path_real2='real222222'

global path_real3
path_real3='Image'

global path_real4
path_real4='word'

class Make():
    def make_graph(self,kidName,kidData,now_date,kidClass2):
        fig, ax = plt.subplots()#그래프틀

        #체온(아동)그리기위해 csv에서 data가공함
        kidData['hour']=kidData['time'].apply( lambda x: int(x.split(":")[0]))
        kidData2=kidData[ kidData['name']==kidName]
        kidData3=kidData2[ kidData['date']==now_date]
        kidData4=kidData3.groupby('hour').mean()
        x1 = kidData4['temp'].keys()
        y1 = kidData4['temp'].values
        list(x1)
        plty1=list(y1)
        plty1=[ round(x,1) for x in plty1]
        xlay1 = [str(x)+"시" for x in list(x1)]
        ylay1 = plty1

        #체온(반평균)그리기위해 csv에서 data가공함
        df2=kidData[ kidData['date']==now_date]
        df3=df2[ kidData['class']==kidClass2]
        df4=df3.groupby('hour').mean()
        x = df4['temp'].keys()
        y = df4['temp'].values
        list(x)
        plty=list(y)
        plty=[ round(x,1) for x in plty]
        xlay = [str(x)+"시" for x in list(x)]
        ylay = plty
        plt.ylim(34, 40)

        #체온(아동)그래프그림
        plot = plt.bar(xlay1, ylay1, label="{0}".format(kidName), color="sandybrown")
        plt.xticks(fontsize = 15, color = 'k')
        plt.xlabel('37.3℃가 넘을경우 색상이 강조됩니다.',fontsize=12)
        plt.yticks(fontsize = 15, color = 'k')

        #그래프 색상조건
        for i in range(len(ylay1)):
            if ylay1[i] >=37.3:
                col = 'crimson'
            else:
                col = 'sandybrown'
            plt.bar(xlay1[i],ylay1[i],color=col)
        #그래프 값출력
        for value in plot:
            height = value.get_height()
            ax.text(value.get_x() + value.get_width()/2.,
                    1.002*height, height, ha='center', va='bottom', size=15)

        #기존그래프에 새그래프 추가함
        plot = plt.plot(xlay, ylay, marker='o', label="반평균", linewidth=4, markersize=8, color='darkblue')
        plt.title('{0} / 반 평균체온'.format(kidName), fontsize=20)
        plt.ylim(34, 40)
        plt.yticks(fontsize = 15, color = 'k')
        plt.legend(fontsize=14)

        return fig.canvas 

class MyBox(BoxLayout):
    def __init__(self,**kwargs):
        super(MyBox,self).__init__(orientation='vertical')
        #변수에 어린이이름/전체엑셀데이터 추가
        self.kidName='배주현'
        self.kidData=pd.read_csv(f"{dirname(__file__)}/temp.csv", encoding='cp949')
        self.make = Make()
        #데이터에서 유니크날짜뽑아서 스피너 꾸미기
        date_list = list(self.kidData['date'].unique())
        self.kidClass = self.kidData.loc[self.kidData['name'] == self.kidName,['class']]
        self.kidClass_list = list(self.kidClass['class'].unique())
        self.kidClass2 = self.kidClass_list[0]
        self.mySpinner = Spinner(text=date_list[-1], values=(date_list))
        self.mySpinner.size_hint  = (0.3, 0.05)
        self.mySpinner.background_color = [250,250,250,1]
        self.mySpinner.color = [0,0,0,1]

        self.mySpinner.pos_hint={'right': 1, 'top':1}
        #스피너에 함수추가
        self.mySpinner.bind(text=self.spinner_change)
        #박스에 스피너추가
        self.add_widget(self.mySpinner)
        
        #그래프추가
        self.graph = Make().make_graph(self.kidName,self.kidData,self.mySpinner.text,self.kidClass2)
        self.add_widget(self.graph)

    def spinner_change(self,widget,value):
        #기존그래프 제거
        self.remove_widget(self.graph)
        #새 그래프 이름도 self.graph로 재생성후 add_widget
        self.graph = self.make.make_graph(self.kidName,self.kidData,self.mySpinner.text,self.kidClass2)
        self.add_widget(self.graph)


class FirstScreen(Screen): #login Screen
    def do_login(self, usernameText, passwordText): #do_login 함수에 loginText, passwordText입력받아라.
        username = ObjectProperty(None)
        password = ObjectProperty(None)
        username = usernameText
        password = passwordText
        info = self.ids.info
        if username == "" and password == "":
            invalidLogin()       
        elif username == "1" and password == "1":
            self.manager.current = 'second'
        elif username == "2" and password == "2":
            self.manager.current = 'third'
        elif db.validate(self.username.text, self.password.text):
            SecondScreen.current = self.username.text and self.password.text
            self.reset()
            self.manager.current = "second"
        else:
            print("")

    def signup(self):
        self.reset()
        self.manager.current = 'signup'

    def reset(self):  
        self.username.text = "" 
        self.password.text = ""

    def on_close(self, *args):
        '''Event handler to "Close" button
    '''
        App.get_running_app().stop()
# ===========================================================================
from kivy.uix.popup import Popup
from database import DataBase
from kivy.uix.label import Label
class SignupScreen(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    parentname = ObjectProperty(None)
    childrenname = ObjectProperty(None)

    def submit(self): 
        if self.username.text == "":
            invalidForm1()
        elif self.username.text != "" or self.password.text != "":  
            db.add_user(self.username.text, self.password.text, self.parentname.text, self.childrenname.text)
            self.reset()
            self.manager.current = "signup"
        else:
            invalidForm()
            
    def login(self):
        self.reset()
        self.manager.current = "first"

    def reset(self):
        self.password.text = ""
        self.username.text = ""
        self.parentname.text = ""
        self.childrenname.text = ""


def invalidLogin():
    pop = Popup( title= "로그인" ,
                 content=Label(text='아이디/비밀번호 확인하세요'),
                  size_hint=(None, None), size=(300, 100),  background = 'popup.png')
    pop.open()

def invalidForm():
    pop = Popup(  title= "회원가입" ,
                 content=Label(text='등록된 아이디 입니다.'),
                  size_hint=(None, None), size=(300, 100),  background = 'popup1.png')   
    pop.open()

def invalidForm1():
    pop = Popup(  title= "회원가입" ,
                 content=Label(text='아이디를 입력하세요.'),
                  size_hint=(None, None), size=(300, 100),  background = 'popup1.png')   
    pop.open()

#그림 띄우기
class Img(Image):
    path3 = StringProperty(f"{dirname(__file__)}/draw/IMG_20200530_183509.png")
    def on_state(self, instance, value):
        global path_real3
        path_real3 = instance
        return super().on_state(instance, value)

class Rv3(RecycleView):
    def __init__(self, **kwargs):
        super(Rv3, self).__init__(**kwargs)
        list___ = ListProperty([])
        plimg.FuncImg()
        list___ = plimg.FuncImg.file_list
        
        for item in list___:
            self.data.append({'text':str(item),'font_name':'HANDotum'} )#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):# 셀렉트 리스트 화면 구성
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel3(RecycleDataViewBehavior, Label):#셀렉트 리스트가 동작 하는것을 감지 하는 클래스
    def __init__(self,**kwargs):
        super(SelectableLabel3,self).__init__()
        self.m3 = plimg.FuncImg()
        self.realpath3 = os.path.realpath('.')

    ''' Add selection support to the Label '''
    index = None
    
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel3, self).refresh_view_attrs(
            rv, index, data)
    
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel3, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global path_real3
        ''' Respond to the selection of items in the view. '''        
        self.selected = is_selected
        if is_selected:            
            path_real.source = f"{dirname(__file__)}/draw/" + rv.data[index]['text']

#단어 띄우기
class Word(Image):
    path4 = StringProperty(f"{dirname(__file__)}/word/IMG_20200530_183720.png")
    def on_state(self, instance, value):
        global path_real4
        path_real4 = instance
        return super().on_state(instance, value)

class Rv4(RecycleView):
    def __init__(self, **kwargs):
        super(Rv4, self).__init__(**kwargs)
        list___w = ListProperty([])
        plword.FuncWord()
        list___w = plword.FuncWord.file_list
        for item in list___w:
            self.data.append({'text':str(item),'font_name':'HANDotum'} )#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):# 셀렉트 리스트 화면 구성
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel4(RecycleDataViewBehavior, Label):#셀렉트 리스트가 동작 하는것을 감지 하는 클래스
    def __init__(self,**kwargs):
        super(SelectableLabel4,self).__init__()
        self.m4 = plword.FuncWord()
        self.realpath4 = os.path.realpath('.')

    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel4, self).refresh_view_attrs(
            rv, index, data)
    
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel4, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global path_real4
        ''' Respond to the selection of items in the view. '''        
        self.selected = is_selected
        if is_selected:            
            path_real.source = f"{dirname(__file__)}/word/" + rv.data[index]['text']
        else:
            print("selection removed for {0}".format(rv.data[index]))

#비디오
class Vid(VideoPlayer):
    path = StringProperty(f"{dirname(__file__)}/covid.avi")
    def on_state(self, instance, value):
        global path_real
        path_real = instance
        # print(instance.source)        
        # print(value)
        return super().on_state(instance, value)
        
class Rv(RecycleView):
    def __init__(self, **kwargs):
        super(Rv, self).__init__(**kwargs)
        list_ = ListProperty([])
        pl.FuncMp3()
        list_ = pl.FuncMp3.file_list
        # self.data = [{'text':str(i)} for i in fm.Func_Class.file_list]#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)
        for item in list_:
            self.data.append({'text':str(item),'font_name':'HANDotum'} )#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)

####################셀렉트 만들기########################
    pass
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):# 셀렉트 리스트 화면 구성
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):#셀렉트 리스트가 동작 하는것을 감지 하는 클래스
    def __init__(self,**kwargs):
        super(SelectableLabel,self).__init__()
        self.m = pl.FuncMp3()
        self.realpath = os.path.realpath('.')

    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)
    
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global path_real
        ''' Respond to the selection of items in the view. '''        
        self.selected = is_selected
        if is_selected:            
            path_real.source = f"{dirname(__file__)}/mp4/" + rv.data[index]['text']
        else:
            print("selection removed for {0}".format(rv.data[index]))

#비디오_두번째
class Vid2(VideoPlayer):
    path2 = StringProperty(f"{dirname(__file__)}/covid.avi")
    def on_state(self, instance, value):
        global path_real2
        path_real2 = instance
        return super().on_state(instance, value)
    
class Rv2(RecycleView):
    def __init__(self, **kwargs):
        super(Rv2, self).__init__(**kwargs)
        list__ = ListProperty([])
        pl.FuncMp3()
        list__ = pl.FuncMp3.file_list
        # self.data = [{'text':str(i)} for i in fm.Func_Class.file_list]#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)
        for item in list__:
            self.data.append({'text':str(item),'font_name':'HANDotum'} )#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)

####################셀렉트 만들기########################
    pass
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):# 셀렉트 리스트 화면 구성
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel2(RecycleDataViewBehavior, Label):#셀렉트 리스트가 동작 하는것을 감지 하는 클래스
    def __init__(self,**kwargs):
        super(SelectableLabel2,self).__init__()
        self.m2 = pl.FuncMp3()
        self.realpath2 = os.path.realpath('.')

    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel2, self).refresh_view_attrs(
            rv, index, data)
    
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        global path_real2
        ''' Respond to the selection of items in the view. '''        
        self.selected = is_selected
        if is_selected:            
            path_real2.source = f"{dirname(__file__)}/mp4/" + rv.data[index]['text']
        else:
            print("selection removed for {0}".format(rv.data[index]))

class SignupScreen(Screen):
    pass

class Actionbar(Widget):
    pass
class SecondScreen(Screen):
    pass

class GraphScreen(Screen):
    pass

class DrawingScreen(Screen):
    pass

class InputScreen(Screen):
    pass

class VideoScreen(Screen):
    pass
class ThirdScreen(Screen):    
    pass

            
#드로잉용 임포트
from kivy.graphics import Rectangle, Color, Line
from random import random
from datetime import datetime
from kivy.graphics import Line, Color, InstructionGroup

#inputword 임포트
from selectiontool import SelectionTool

class ChildrenScreen(Screen):    
    pass

class KidDrawingScreen(Screen):
    undolist = []
    objects = []
    drawing = False

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_down(self, touch): 
        super(KidDrawingScreen, self).on_touch_down(touch) 

        with self.canvas:
            Color(random(), random(), random()) #색 랜덤으로 바꾸기
            self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2) #포인터 위치 지정

    def on_touch_move(self, touch):
        if self.drawing:
            self.points.append(touch.pos)
            self.obj.children[-1].points = self.points
        else:
            self.drawing = True
            self.points = [touch.pos]
            self.obj = InstructionGroup()
            self.obj.add(Color(random(), random(), random()))
            self.obj.add(Line(width=2))
            self.objects.append(self.obj)
            self.canvas.add(self.obj)

    def undo(self):
        if len(self.objects) != 0:
            item = self.objects.pop(-1)
            self.undolist.append(item)
            self.canvas.remove(item)

    def clear_canvas(self): # 캔퍼스를 지우는 기능. 캔퍼스는 투명도 0으로 만드어놨기때문에 보이지는 않지만, 지우는 기능은 가능하다. 
        self.canvas.clear()

    def Ss(self): 
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.export_to_png(f"{dirname(__file__)}\draw\IMG_"+timestr+".png")

class KidInputScreen(Screen):
    def __init__(self, **kwargs): #
        super(KidInputScreen,self).__init__(**kwargs)
        self.kp = SelectionTool() #네모 그리는 클래스 가져옴
        self.add_widget(self.kp)

class KidVideoScreen(Screen):
    pass

class Manager(ScreenManager):
    pass
db = DataBase(f"{dirname(__file__)}/users.csv")

class CoronaApp(MDApp):
    username = StringProperty(None) # 이름 입력값
    password = StringProperty(None) # P/W 입력값
    
    def build(self):
        return Manager()

if __name__ == '__main__':
    CoronaApp().run()