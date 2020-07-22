# 학생/학부모를 위한 코로나19 모니터링 앱 개발
<br>
<img src="/images/project_show.jpg">


- 본 프로젝트를 통해 코로나블루 대처를 위한 스마트 로봇 및 어플 개발 기사가
영남일보에 게재 되었습니다.  
(2020-06-20)&nbsp;[영남일보기사](https://www.yeongnam.com/web/view.php?key=20200602001339189)

<img src="/images/covid_project.jpg" width="70%">

# 


## 1. 개발 취지
- 코로나19 바이러스 확산에 따른 전국 초중고교의 개학이 전면 연기되었습니다.(20.3월)
- 바이러스의 펜데믹이 지속되고 있으나 개학을 지속 연기할 수는 없는 상황에 다다르게 되었고,
  순차적 개학이 추진됨에 따라 자녀를 학교에 보내야 하는 부모님들의 걱정 또한 날로 증가하게
  되었습니다.
- 아이들의 등교 후 발열상태 확인, 추적 관찰에 대한 필요성이 대두되었습니다.
- 이에 체온 측정, 동선 파악, 표정상태, 심리상태 등을 쉽게 파악하고 모니터링 할 수 있는
  앱 개발을 추진하게 되었습니다.

## 2. 개발 필요 기능
- 등교 시 자녀의 체온 자동 측정, 이후 지속적인 체온 측정이 실시되었으면 좋겠음.
- 체온 측정 시 모습을 동영상으로 기록하여, 아이의 상태를 육안으로 확인하면 좋겠음.
- 체온이 측정된 위치를 파악하여, 측정 당시 동선 및 주변 접촉자 파악이 용이하였으면 좋겠음.
- 아이의 심리상태를 파악하기 위해 그림그리기나 단어입력놀이 기능을 추가하였으면 좋겠음.

## 3. 구현 방법 검토
### (1) 체온 측정, 동영상 녹화, 위치 파악
- 아이들에게 친숙한 펭수 인형을 활용, 인형 하단에 주행가능한 Robot을 부착하는 형태
    + 인형 내부에 구동용 라즈베리파이 보드 + Touch Display + 웹캠 + 열감지 센서를 부착함
    + 하단 주행 Robot에는 주행 중 충격 발생 시 회피 기능 추가

### (2) 체온 상태, 아이 모습, 위치 파악, 그림그리기, 단어 입력
- 모바일/윈도우 앱을 이용하여 부모/아이/관리자(선생님)용 모니터링 화면을 각각 개발

## 4. 개발 Tool 선정
- 프로그래밍 언어 : Python + TKinter
    + 선정이유 : 범용성, 확장성 용이. 언어 접근성 용이. Python 초보의 UI 구현을 위해 프로젝트에 도입.
- 하드웨어 : 라즈베리파이
- OS : 우분투

## 5. 팀별 업무 분장
### (1) 로봇팀 : 펭수 로봇 개발 
- 주행 Robot 조립 및 구동용 보드 연계
- Robot 조작 프로그램 구현
- 아이 얼굴 인식, 열화상 체크, GPS 위치값 저장 기능 구현
- 아이들에게 낯설지 않고 친숙하게 다가가기 위해 Touch화면에 구동 가능한 노래, 동영상 재생

### (2) 앱개발 팀 : 체온 모니터링 앱 개발
- 회원가입 / 로그인 창 구현
- 체온 정보 그래프, 반 평균 체온 그래프, 37.3℃ 이상 감지 시 Warning 기능 구현
- 체온 측정 시간의 아이 동영상 재생 기능 구현
- 화면 터치를 통해 그림그리기 및 단어입력 가능한 폼 구현

#### (*본 프로젝트 중 앱개발팀 과정만 서술하였습니다.)

## 6. 코드 구현(python + TKinter)
- 최소한의 구동이 가능한 수준에서의 개발을 1차 목표로 하여 간결한 화면 위주로 진행하였습니다.

main.py
```python
from tkinter import*
import math
from tkinter import messagebox
import tkinter as tk
import tkinter.ttk as ttk
import os
import PIL
from PIL import Image,ImageTk
import datetime
import subprocess
# import pront2
# from pront2 import *
import numpy as np
import cv2

class Login: #로그인 전용 클래스 생성
    def __init__(self, window): #init으로 로그인화면 초기화 진행
        self.window = window #밑에서 받아올 윈도우를 self.window로 지정
        self.mainframe = Frame(self.window) #self.window의 frame을 self.mainframe으로 지정
        self.mainframe.pack(fill = "both", expand=YES) #self.mainframe을 pack형태로 나타냄
        self.str1 = StringVar() #String 타입의 self.str1을 생성
        self.str2 = StringVar() #String 타입의 self.str2를 생성
        self.L1 = Label(self.mainframe, text="ID : ") #Self.mainframe안에 "ID : "문자값을 가진 self.L1이라는 Label을 생성
        self.L2 = Label(self.mainframe, text="비밀번호 : ") #Self.mainframe안에 "ID : "문자값을 가진 self.L1이라는 Label을 생성
        self.textbox1 = Entry(self.mainframe, width=15, textvariable=self.str1)
        #Self.mainframe안에 텍스트창을 만들고, self.str1값으로 받아옴
        self.textbox2 = Entry(self.mainframe, width=15, textvariable=self.str2)
        #Self.mainframe안에 텍스트창을 만들고, self.str2값으로 받아옴
        self.L1.pack(side=LEFT) #L1 라벨을 나타냄
        self.textbox1.pack(side=LEFT) #textbox1 텍스트창을 나타냄
        self.L2.pack(side=LEFT) #L2 라벨을 나타냄
        self.textbox2.pack(side=LEFT) #textbox2 텍스트창을 나타냄
        self.action=ttk.Button(self.mainframe, text="로그인", command=self.clickMe)
        #self.mainframe안에 "로그인" 적힌 버튼을 action이라는 이름으로 생성하되, 클릭시 self.clickMe 함수를 실행시킴
        self.action.pack(side=LEFT) #action(버튼)을 나타냄
        
    def clickMe(self):#clickMe라는 함수를 생성함
        if self.str1.get() == 'a' and self.str2.get() == 'a' : 
            #str1값이 a와 일치하고 str2값이 a와 일치할 경우(and 조건)
            messagebox.showinfo("로그인성공", self.str1.get()+ "님 환영합니다!")
            #로그인성공창 띄우고, str1값 가져옴
            self.mainframe.destroy()#mainframe창을 없앰
            usermode.second()#second 함수 실행함
        elif self.str1.get() == 'b' and self.str2.get() == 'b' :
            messagebox.showinfo("로그인성공", "관리자님 환영합니다!")
            self.mainframe.destroy()
            powermode.third()#third 함수 실행함
        elif self.str1.get() == 'c' and self.str2.get() == 'c' :
            messagebox.showinfo("로그인성공", "관리자님 환영합니다!")
            self.mainframe.destroy()
            powermode.forth()#forth 함수 실행함
        else:
            messagebox.showinfo("로그인실패", "ID, 비밀번호가 잘못되었습니다.")
            #아닐경우 로그인실패창 띄움

window = Tk()
window.title("로그인화면")
window.geometry('400x750')

mainframe = Login(window)


class usermode : 
    def second():#second 함수 
        top_frame=Frame(window)#인물정보를 나타낼 윈도우 상의 top_frame을 지정
        top_frame.pack(fill = "both", expand=YES)#top_frame을 pack형태로 나타냄(전체로 채움, 빈영역할당)

        bottom_frame=Frame(window)#체온정보를 나타낼 윈도우 상의 bbttom_frame을 지정
        bottom_frame.pack(side=TOP, fill=BOTH, expand=YES)
        #bottom_frame을 pack형태로 나타냄(왼쪽에 배치, 전체로 채움, 빈영역할당)
    
        frame_1 = Frame(top_frame, background="white", relief="groove", bd=2)#사진프레임
        #top_frame안에 frame_1이라는 이름의 frame을 지정(배경 흰색, relief는 얇은선형태, bd는 테두리두께)
        frame_1.pack(side=LEFT, fill=BOTH, expand=YES)#frame_1을 pack형태로 나타냄

        frame_2=Frame(top_frame, relief="groove", bd=2)
        #top_frame안에 frame_2이라는 이름의 frame을 지정(배경 흰색, relief는 얇은선형태, bd는 테두리두께)
        frame_2.pack( side=LEFT, fill=BOTH, expand=YES)#frame_1을 pack형태로 나타냄

        photo = PhotoImage(file = "e.png").subsample(2) 
        label7 = Label(frame_1,image = photo, width=100, height=100)
        label7.image = photo
        label1 = Label(frame_2, text = "이름 : 정아름(6)")
        name = StringVar()
        print(name)
        label2 = Label(frame_2, text = "반 : 토끼반(김선녀 선생님)")
        group = StringVar()
        print(group)
        label3 = Label(frame_2, text="부모명 : 김태희 님")
        parents = StringVar
        print(parents)
        # label4 = Label(frame_2, text = "나이");
        # age = StringVar()
        # print(age)
        # label5 = Label(frame_2, text = "선생님");
        # teacher = StringVar
        # print(teacher)
        label6 = Label(frame_2, text="연락처 : 010-1111-2222")
        phone = StringVar
        print(phone)

        #출력창
        label7.pack(side = TOP);

        label1.pack(side = TOP );
        label2.pack(side = TOP);
        label3.pack(side = TOP);
        # label4.pack(side = TOP);
        # label5.pack(side = TOP);
        label6.pack(side = TOP);

        # font(글꼴,크기) , fg = 글씨 색깔 , bg = 뒷배경 색깔
        
        #메뉴탭 체온,기분상태


        notebook=tk.ttk.Notebook(bottom_frame)
        notebook.pack(fill = "both")

        frame1=tk.Frame(window)
        notebook.add(frame1, text="체온")

        label8=tk.Label(frame1, text="측정시간별 체온")
        label8.pack()

        width = 360
        height = 300

        def cc() :
            treeview.tag_configure("tag2", background="red")

        treeview=tk.ttk.Treeview(frame1, columns=["one", "two"], 
        displaycolumns=["two", "one"])
        treeview.pack()

        treeview.column("#0", width=70)
        treeview.heading("#0", text="num")

        treeview.column("one", width=100, anchor="center")
        treeview.heading("one", text="체온", anchor="center")

        treeview.column("#2", width=100, anchor="w")
        treeview.heading("two", text="측정시간", anchor="center")

        treelist=[(37.2, "2020-05-04 10:30:10"), (37.1, "2020-05-04 11:05:10"), 
        (36.9, "2020-05-04 11:45:17"), (36.8, "2020-05-04 12:15:38"), (36.5, "2020-05-04 12:57:12")]

        for i in range(len(treelist)):
            treeview.insert('', 'end', text=i, values=treelist[i], iid=str(i)+"번")

        treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=cc)

        print()
        label9=tk.Label(frame1, text="그래프로 보기")
        label9.pack()

    #그래프 추가위치===================================================================================
        canvas = Canvas(frame1, width=width, height=height, bg='white')
        canvas.pack()

        line=canvas.create_line(50, 10, 50, 290, fill="black")
        line=canvas.create_line(20, 270, 400, 270, fill="black")
        polygon=canvas.create_polygon(70, 130, 100, 130, 100, 270, 70, 270, fill="orange", outline="red")
        polygon=canvas.create_polygon(110, 140, 140, 140, 140, 270, 110, 270, fill="orange", outline="red")
        polygon=canvas.create_polygon(150, 150, 180, 150, 180, 270, 150, 270, fill="orange", outline="red")
        polygon=canvas.create_polygon(190, 135, 220, 135, 220, 270, 190, 270, fill="orange", outline="red")
        polygon=canvas.create_polygon(230, 120, 260, 120, 260, 270, 230, 270, fill="orange", outline="red")

    #그래프 끝===================================================================================

    #로그아웃 함수 및 버튼 생성=======================================
        def evend_logout(event):
            bottom_frame.destroy()
            top_frame.destroy()
            Login(window)
        button2 = Button(bottom_frame,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)
    #로그아웃 함수 및 버튼 종료=======================================


#표정 시작===================================================================================

        frame2=tk.Frame(window)
        notebook.add(frame2, text="기분상태")

        label10=tk.Label(frame2, text="표정별 기분상태")
        label10.pack()

        frameface=Frame(frame2, background="white",relief="groove", bd=1)
        frameface.pack(side=RIGHT, fill=BOTH, expand=YES)

        frametime=Frame(frame2, background="gray",relief="groove", bd=1)
        frametime.pack(side=LEFT, fill=BOTH, expand=YES)

        detection_time_label = Label(fra3metime,text="2020-05-06 09:30", relief="groove", bd=2)
        detection_time_label.pack()    
        
        facephoto = PhotoImage(file = "e.png") 
        label11 = Label(frame2,image = facephoto ,width=100, height=100)
        label11.image = facephoto
        label11.pack(side=TOP)

        time_label = Label(frametime, text="2020-05-04 10:30:10")
        time_label.pack()
        frame_of_face = Frame(frame2,relief="groove")
        frame_of_face.pack(side=LEFT)

        analysis_face = ['happyness: 40%','sadness:20%','depression:5%','violence: 0%']
        values = StringVar(value=analysis_face)
        listbox = Listbox(master=frameface, listvariable=values)
        listbox.pack(fill=BOTH)

    #표정 끝===================================================================================

#관리자모드 시작, 실시간==============================================

class powermode : 
    def third() : 
        notebook=tk.ttk.Notebook(window, width=390, height=390)
        notebook.pack()

        frame1=tk.Frame(window)
        notebook.add(frame1, text="실시간")

        f2=Frame(frame1)#인물정보를 나타낼 윈도우 상의 top_frame을 지정
        f2.pack(fill = "both", expand=YES)

        label1=tk.Label(f2,text='cam')
        label1.place(relwidth = 1, relheight=1)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 450)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 450)
        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label1.imgtk = imgtk
            label1.configure(image=imgtk)
            label1.after(10, show_frame)

        show_frame()

        def evend_logout(event):
            print("성공")
            frame1.destroy()
            frame2.destroy()
            notebook.destroy()
            Login(window)
        button2 = Button(frame1,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)

        frame2=tk.Frame(window)
        notebook.add(frame2, text="학생")

        label2=tk.Label(frame2, text="페이지2의 내용")
        label2.pack()

    #로그아웃 함수 및 버튼 생성=======================================
        def evend_logout(event):
            frame1.destroy()
            frame2.destroy()
            notebook.destroy()
            Login(window)
        button2 = Button(frame2,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)
    #로그아웃 함수 및 버튼 종료=======================================

    #관리자모드끝==============================================

    #관리자모드2 시작==============================================

    def forth():
        def silsigan():
            cap = cv2.VideoCapture(0)

            while(True):
                # Capture frame-by-frame
                ret, frame1 = cap.read()

                # Our operations on the frame come here
                gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

                # Display the resulting frame
                cv2.imshow('frame1',gray) #imshow = 이미지출력
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # When everything done, release the capture
            # cap.release()
            cv2.destroyAllWindows()

        notebook=tk.ttk.Notebook(window, width=390, height=390)
        notebook.pack()

        frame1 = Frame(window)
        notebook.add(frame1, text="실시간")
        notebook.pack()

        frame2 = Frame(window)
        notebook.add(frame2, text="두번째탭")
        notebook.pack()

        button1 = Button(frame1,text="실시간 영상",command=silsigan)
        button1.pack()
    #관리자모드2 끝==============================================

    #로그아웃 함수 및 버튼 생성=======================================
        def evend_logout(event):
            frame1.destroy()
            frame2.destroy()
            Login(window)
        button2 = Button(mainframe,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)
    #로그아웃 함수 및 버튼 종료=======================================
window.mainloop()
```
<img src="/images/tk_login.jpg" width="30%">&nbsp;<img src="/images/main.jpg" width="30%"><br>
<img src="/images/face.jpg" width="30%">&nbsp;<img src="/images/cam.jpg" width="30%"><br>
<br>

## 7. 코드 구현 후 문제점
- python 개발 지식의 부족으로 생각했던 기능 대부분을 제대로 구현할수 없었습니다.
    + DB에서 데이터를 불러와서 처리하는 방식으로 구현을 해야 했으나, 그 방법을 몰라 sorce 코드에 직접 입력하는 상수 형태로
    구현할 수 밖에 없었습니다.(로그인, 체온정보 불러오기, 인물정보 불러오기 등)
    + 그래프를 plot 형태로 그려야 했으나, 방법을 몰라 4개의 점을 잇는 line 형태로 그리게 되었습니다.
    + 동영상 불러오는 방법을 몰라 웹캠 화면을 직접 불러들이는 코드로 변경하게 되었습니다.
    + 관리자 페이지는 대부분 구현을 못했습니다.
    + TKinter의 UI상 한계로 원하는 곳에 원하는 개체를 배치하지 못했습니다.

- 이에 실력을 좀 더 키우고, UI적 접근이 용이한 Kivy를 활용하여 재 코딩하게 되었습니다.


## 8. Re-programming(python - Kivy)
### (1) Kivy 특징 
- source 코드와 UI 코드가 분리되어 있어, 각자 부분만 집중해서 개발할 수 있습니다.(.py 파일, .kv파일)
- TKinter보다 기능적인 UI 포맷이 많습니다.

### (2) 메뉴 재구성
- 부모용 / 아이용 화면을 로그인 단계에서 분리하고, 관리자용은 필요시 추가 개발하는 것으로 하였습니다.
- 부모용에는 체온보기/그림보기/단어보기/동영상보기의 4가지 메뉴로 구성하기로 하였습니다.
- 아이용에는 그림그리기/단어입력/동영상보기의 3가지 메뉴로 구성하기로 하였습니다.
- 아이용에서 그린 그림과 단어입력화면을 저장하면, 부모용 메뉴에서 볼수 있는 형태로 개발하기로 하였습니다.

### (3) 코드 구현(python + Kivy)

main.py
```python
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
```
<br>
switch.kv

```python
#:kivy 1.10.0
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<SBt@Button>
    background_color: (0,0,0,0)
    background_normal:''
    back_color:(0.9,0.5,0.8,1)
    border_radius:[18]
    canvas.before:
        Color:
            rgba:self.back_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:self.border_radius

<StrokeBt@Button>
    background_color: (0,0,0,0)
    background_normal:''
    back_color:(0.9,0.8,0.8,1)
    border_radius:[18]
    # color:self.back_color
    # bold:True
    canvas.before:
        Color:
            rgba:self.back_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:self.border_radius
        # Color:
        #     rgba:self.back_color
        # Line:
        #     rounded_rectangle:(self.pos[0],self.pos[1],self.size[0],self.size[1],self.border_radius) 
        #     width:1.2

<SignupBt@Button>
    
    background_color: (0,0,0,0)
    background_normal:''
    back_color:(0.9,0.5,0.8,1)
    border_radius:[18]
    # color:self.back_color
    # bold:True
    canvas.before:
        Color:
            rgba:self.back_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:self.border_radius

<SBt2@Button>
    background_color: (0,0,0,0)
    background_normal:''
    back_color:(1,1,1,1)
    border_radius:[10]
    source_img:'kivy/graph.png'
    canvas.before:
        Color:
            rgba:self.back_color
        RoundedRectangle:
            size:self.size
            pos:self.pos
            radius:self.border_radius
            source:self.source_img


<Manager>:
    transition: FadeTransition()
    FirstScreen:
        id:screen_1
        name: 'first'
    SignupScreen:
        id:screen_1_1
        name: 'signup'
    SecondScreen:
        id:screen_2
        name:'second'
    DrawingScreen:
        id:screen_2_1
        name:'second_drawing'
    GraphScreen:
        id:screen_2_2
        name:'second_graph'
    InputScreen:
        id:screen_2_3
        name: 'second_input'
    VideoScreen:
        id:screen_2_4
        name: 'second_video'
    

    ChildrenScreen:
        id:screen_3
        name:'third'
    KidDrawingScreen:
        id:screen_3_1
        name:'third_drawing'
    KidInputScreen:
        id:screen_3_2
        name: 'third_input'
    KidVideoScreen:
        id:screen_3_3
        name: 'third_video'
<FirstScreen>:
    username: username
    password: password
    FloatLayout:
        canvas.before:
            Rectangle:
                pos:self.pos
                size:self.size
                source:'main.png'
    FloatLayout:
        
        size_hint:1,1
        Label:
            id: info
            text: ''
            markup: True
            size_hint_y: 1.28
            font_size: 20
            height: 100
        TextInput:        
            id: username    
            multiline:False
            font_size: 15
            size_hint:0.55, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.67}
            hint_text:'ID'
            font_size: 15
            multiline: False
            focus: True
            on_text_validate: password.focus = True
        TextInput:
            id: password
            multiline:False
            password:True
            font_size: 15
            hint_text:'PASSWORD'
            size_hint:0.55, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.60}
            font_size: 15
            multiline: False
            focus: True
            on_text_validate: root.firstscreen()
        SBt:
            canvas:
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:'login.png'
            size_hint:0.3,0.06
            pos_hint:{'center_x':0.337,'center_y':0.53}
            back_color:(0.156,0.455,0.753,1.0)
            on_press:root.do_login(username.text, password.text)
        StrokeBt:
            canvas:
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:'exit.png'
            size_hint:0.3,0.06
            pos_hint:{'center_x':0.657,'center_y':0.53}
            back_color:(1,0.155,0.553,1.0)
            on_press: root.on_close() 
        SignupBt:
            canvas:
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:'signup.png'
            size_hint:0.3,0.06
            pos_hint:{'center_x':0.5,'center_y':0.45}
            back_color:(0.156,0.455,0.753,1.0)
            on_press: root.signup()
# ========================================================================
<SignupScreen>:

    username: username
    password: password
    parentname: parentname
    childrenname: childrenname
    FloatLayout:
        canvas:
            Rectangle:
                pos:self.pos
                size:self.size
                source:'main.png'
    FloatLayout:
        
        BoxLayout:
            orientation: 'horizontal'
            Label:
                size_hint: 0.2,0.35
            Label:
                font_size: 20
                text: '부모님용'
                color: 0,0,0,5
                size_hint: (0.4, 0.35)
                pos_hint:{'center_x':0.5,'center_y':0.68}
            CheckBox:
                # name: name1
                group: 'a'
                size_hint: (0.4, 0.35)
                pos_hint:{'center_x':0.5,'center_y':0.68}
                color: 0,0,0,1
            Label:
                size_hint: 0.2,0.35
            Label:
                font_size: 20
                text: '아이용' 
                color: 0,0,0,5
                size_hint: (0.4, 0.35)
                pos_hint:{'center_x':0.5,'center_y':0.68}
            CheckBox:
                # name: name2
                group: 'a'
                size_hint: (0.4, 0.35)
                pos_hint:{'center_x':0.5,'center_y':0.68}
                color: 0,0,0,1 
            Label:
                size_hint: 0.2,0.35
        TextInput:
            id: username
            multiline:False
            font_size: 15
            size_hint:0.65, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.60}
            hint_text:'아이디'
            font_size: 15
            multiline: False
            focus: True
            on_text_validate: password.focus = True
        TextInput:
            id: password
            multiline:False
            password:True
            font_size: 15
            hint_text:'비밀번호'
            size_hint:0.65, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.52}
            font_size: 15
            multiline: False
            focus: True
            on_text_validate: root.firstscreen()

        TextInput:
            id: parentname    
            multiline:False
            font_size: 15
            size_hint:0.65, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.44}
            hint_text:'부모님성함'
            font_size: 15
        TextInput:
            id: childrenname    
            multiline:False
            font_size: 15
            size_hint:0.65, 0.05
            pos_hint:{'center_x':0.5,'center_y':0.36}
            hint_text:'아이이름'
            font_size: 15   
        SBt:
            canvas:
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:'submit.png'
            size_hint:0.3,0.06
            pos_hint:{'center_x':0.337,'center_y':0.28}
            back_color:(0.156,0.455,0.753,1.0)
            on_release: 
                root.manager.transition.direction = "left"
                root.submit()
        StrokeBt:
            canvas:
                Rectangle:
                    pos:self.pos
                    size:self.size
                    source:'cancel.png'
            size_hint:0.3,0.06
            pos_hint:{'center_x':0.657,'center_y':0.28}
            back_color:(1,0.155,0.553,1.0)
            on_release:
                root.manager.transition.direction = "left"
                root.login()
# ========================================================================
<SecondScreen>:
    GridLayout:
        rows: 5
        orientation:"vertical"
        canvas.before:
            Color:
                rgba: 0.2, .2, .2, 1
            Rectangle:
                pos: 0, 0
                size: self.size
        ActionBar:
            pos_hint: {'top': 1}
            
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "배주현부모님 반갑습니다!"
                    with_previous: False
                ActionButton:
                    text: "로그아웃"
                    on_press:
                        root.manager.current = 'first' 
                        root.manager.get_screen('first').reset()      

        BoxLayout: 
            padding: 2  
            SBt2:
                size_hint:1,1
                source_img:'c1.PNG'
                on_press:root.manager.current = 'second_graph'            
        BoxLayout:
            padding: 2    
            SBt2:
                size_hint:1,1
                source_img:'c2.PNG'
                on_press:root.manager.current = 'second_drawing' 

        BoxLayout:    
            padding: 2
            SBt2:
                text_size: self.size  
                size_hint:1,1
                source_img:'c3.PNG'
                on_press:root.manager.current = 'second_input' 
        BoxLayout:   
            padding: 2
            SBt2:
                text_size: self.size  
                size_hint:1,1
                source_img:'c4.PNG'
                on_press:root.manager.current = 'second_video' 
# ========================================================================  
<DrawingScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:3
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "그림보기"
                    with_previous: False 
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'second' 
        Img:
            source:self.path3
            state:'play'
            options: {'allow_stretch': True}
        Rv3:
            pos_hint:{'x':0,'y':0.1}
            id:rv3            
            data:self.data
            viewclass: 'SelectableLabel3'
            SelectableRecycleBoxLayout:                
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: True

<SelectableLabel3>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size  



<GraphScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:2
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "체온보기"
                    with_previous: False                
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'second' 
        MyBox:
    
<InputScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:3
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "그림보기"
                    with_previous: False 
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'second' 
        Word:
            source:self.path4
            state:'play'
            options: {'allow_stretch': True}
        Rv4:
            pos_hint:{'x':0,'y':0.1}
            id:rv4           
            data:self.data
            viewclass: 'SelectableLabel4'
            SelectableRecycleBoxLayout:                
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: True

<SelectableLabel4>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size  

<VideoScreen>:   
    GridLayout: 
        orientation: "vertical"
        rows:3
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "아이영상"
                    with_previous: False
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'second' 
                        
        Vid:
            source:self.path
            state:"play"
            options: {'allow_stretch': True}
        Rv:
            pos_hint:{'x':0,'y':0.1}
            id:rv            
            data:self.data
            viewclass: 'SelectableLabel'
            SelectableRecycleBoxLayout:                
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: True
    
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size  

#==========================================================================
<ChildrenScreen>:
    GridLayout:
        rows: 4
        orientation:"vertical"
        canvas.before:
            Color:
                rgba: 0.2, .2, .2, 1
            Rectangle:
                pos: 0, 0
                size: self.size
        ActionBar:
            back_color:(0.6,0.6,0.6,0.9)
            pos_hint: {'top': 1}
            
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "배주현아동 반갑습니다!"
                    with_previous: False
                ActionButton:
                    text: "로그아웃"
                    on_press:
                        root.manager.current = 'first' 
                        root.manager.get_screen('first').reset()       
      
        BoxLayout:    
            padding: 10
            SBt2:
                size_hint:1,1
                source_img:'c5.PNG'
                on_press:root.manager.current = 'third_drawing'    
        BoxLayout:   
            padding: 10
            SBt2:
                text_size: self.size  
                size_hint:1,1
                source_img:'c6.PNG'
                on_press:root.manager.current = 'third_input' 
        BoxLayout:   
            padding: 10
            SBt2:
                text_size: self.size  
                size_hint:1,1
                source_img:'c7.PNG'
                on_press:root.manager.current = 'third_video' 


<KidDrawingScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:2
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "그림그리기"
                    with_previous: False
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'third' 
        BoxLayout:
            orientation: 'horizontal'
            Label:  
                size_hint: 0.05, 0.1

            Button:
                background_color: (0,0,0,0)
                canvas:
                    Color:
                        rgba: 1, 1, 1, 1
                    Rectangle:
                        pos:self.pos
                        size:self.size
                        source:'clear.png'
                text: '이전지우기'
                pos_hint: {"center_x":.01, "y":.01} 
                size_hint: 0.05, 0.1
                on_press: 
                    root.undo()
            Label:
                size_hint: 0.05, 0.1

            Button:
                background_color: (0,0,0,0)
                canvas:
                    Rectangle:
                        pos:self.pos
                        size:self.size
                        source:'save1.png'
                text: '저장하기'
                pos_hint: {"center_x":.01, "y":.01} 
                size_hint: 0.05, 0.1
    
                on_press: 
                    root.Ss()
            Label:
                size_hint: 0.05, 0.1
   
<KidInputScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:3
        ActionBar:

            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "단어놀이"
                    with_previous: False
                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'third' 

<KidVideoScreen>:
    GridLayout: 
        orientation: "vertical"
        rows:3
        ActionBar:
            pos_hint: {'top': 1}
            ActionView:
                use_separator: True
                ActionPrevious:
                    title: "내모습보기"
                    with_previous: False

                ActionButton:
                    text: "뒤로가기"
                    on_press:root.manager.current = 'third' 
        Vid2:
            source:self.path2
            state:"play"
            options: {'allow_stretch': True}
        Rv2:
            pos_hint:{'x':0,'y':0.1}
            id:rv2            
            data:self.data
            viewclass: 'SelectableLabel2'
            SelectableRecycleBoxLayout:                
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: True
    
<SelectableLabel2>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.before:
        Color:
            rgba: (.7, .0, .2, .2) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size        
```
<img src="/images/login.jpg" width="30%">&nbsp;
<img src="/images/kivy_main.jpg" width="30%">&nbsp;
<img src="/images/graph1.jpg" width="30%">
<br>
<img src="/images/graph2.jpg" width="30%">&nbsp;
<img src="/images/pic.jpg" width="30%">&nbsp;
<img src="/images/word.jpg" width="30%">
<br>
<img src="/images/movie.jpg" width="30%"><br>
로그인 및 부모용 화면
<br><br>
<img src="/images/main2.jpg" width="30%">&nbsp;
<img src="/images/draw.jpg" width="30%">&nbsp;
<img src="/images/wording.jpg" width="30%">
<br><img src="/images/sign.jpg" width="30%"><br>
회원가입 및 아이용 화면
<br><br>

## 9. kivy 전환 후 변경점
- UI의 촌스러움은 많이 개선되었습니다. 기능 개선도 일부 진행되었습니다.
    + 여전히 DB에서 불러오는 방식은 처리하지 못했습니다. 대신 csv 파일에서 불러오는 형태로 개선되었습니다.
    + 그래프를 원하는 plot 형태로 구현할 수 있게 되었습니다.
    + 화면에 직접 그림을 그리는 기능 + 단어를 입력할 수 있는 기능 + 저장 등의 소소한 기능을 구현할수 있게 되었습니다.
    + 파일리스트에서 선택한 동영상을 재생할 수 있게 되었습니다.

## 10. 총평 

- python으로 코딩하는 것에 대해 기초 지식은 잘 쌓았다(?)고 생각됩니다.
- 원하는 기능을 다 구현하지는 못했지만, 차차 라이브러리를 잘 활용하여 모두 다 구현될 수 있도록 지속 노력해야 겠구나 생각하게 됩니다.


