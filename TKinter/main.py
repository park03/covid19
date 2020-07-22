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