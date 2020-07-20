# 학생/학부모를 위한 코로나19 모니터링 앱 개발


- 본 프로젝트를 통해 코로나블루 대처를 위한 스마트 로봇 및 어플 개발 기사가
영남일보에 게재 되었습니다(2020-06-20)

[영남일보기사](https://www.yeongnam.com/web/view.php?key=20200602001339189)

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

## 6. 코드 구현
- 최소한의 구동이 가능한 수준에서의 개발을 1차 목표로 하여 간결한 화면 위주로 진행하였습니다.

### (1) 로그인 화면

```python
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
        self.textbox2 = Entry(self.mainframe, width=15, textvariable=self.str2, show = '*')
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
```
- textbox에 입력된 값과 code속의 값이 일치할 경우 로그인되는 형태의 간단한 로그인창 구현 

<img src="/images/tk_login.jpg" width="20%">


### (2) 초기 화면
```python
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
        photo = PhotoImage(file = "face.png").subsample(1) #face.png라는 포토이미지를 photo 변수에 넣음(subsample:크기_클수록 작아짐)
        label5 = Label(frame_1,image = photo, width=100, height=100) #frame1안에 photo라는 이미지를 라벨7에 넣음
        label5.image = photo #라벨7의 이미지는 photo임
        label1 = Label(frame_2, text = "이름 : 정아름(6)") #라벨1에 정아름(6)을 입력함, 향후 DB 연동 필요
        name = StringVar() #name이라는 문자열변수 선언
        print(name) #name을 출력함
        label2 = Label(frame_2, text = "반 : 토끼반(김선녀 선생님)")#라벨2에도 동일방식 적용
        group = StringVar() #group이라는 문자열변수 선언
        print(group) #group을 출력함
        label3 = Label(frame_2, text="부모명 : 김태희 님") #라벨3에도 동일방식 적용
        parents = StringVar
        print(parents)
        label4 = Label(frame_2, text="연락처 : 010-1111-2222") #라벨2에도 동일방식 적용
        phone = StringVar
        print(phone)
        label5.pack(side = TOP)
        label1.pack(side = TOP)
        label2.pack(side = TOP)
        label3.pack(side = TOP)
        label4.pack(side = TOP)
```
- 상하단을 프레임으로 나누어 상단에 인물정보, 하단의 체온 정보를 나타냄


### (3) 탭 기능 추가
```python
#탭 출력(notebook)====================================================
        notebook=tk.ttk.Notebook(bottom_frame) #bottom프레임에 notebook(탭)을 생성함
        notebook.pack(fill = "both") #노트북을 배치함
        frame1=tk.Frame(window) #윈도우에 frame1을 생성함
        notebook.add(frame1, text="체온") #노투북에 frame1을 추가(탭추가) 하고 탭 이름을 체온으로 지정
        label6=tk.Label(frame1, text="측정시간별 체온") #frame1안에 "측정시간별 체온"이라는 라벨 추가
        label6.pack() #라벨6 배치
```
- 체온정보/표정정보를 구분하기 위해 탭 기능 구현

### (4) 체온 정보 상세 화면
```python
#체온값 출력============================================================

        def cheon() : #cheon 함수 생성
            treeview.tag_configure("tag2", background="red") #밑에 tag1을 누르면 해당 함수를 실행하며 tag2번의 백그라운드를 red로 바꿈
        treeview=tk.ttk.Treeview(frame1, columns=["one", "two"], 
        displaycolumns=["one", "two"], height=5) #트리뷰에 one,two라는 컬럼을 list형태로 만들고, one, two를 list형태로 출력시킴
        treeview.pack() #트리뷰를 나타냄
        treeview.column("#0", width=70) #트리뷰 컬럼의 순서시작은 #0부터 시작하며 폭은 70임
        treeview.heading("#0", text="No") #첫번째 컬럼의 제목은 No로 지정함
        treeview.column("one", width=130, anchor="center") #두번째 컬럼은 one이라는 이름으로 나타내고 폭은 130, 값은 중앙정렬함 
        treeview.heading("one", text="측정시간", anchor="center") #one 컬럼의 제목은 측정시간이고, 제목을 가운데 정렬함.
        treeview.column("two", width=70, anchor="center") #세번째 컬럼은 two라는 이름으로 나타내고 폭은 70, 내용은 가운데 정렬함.
        treeview.heading("two", text="체온", anchor="center") #two 컬럼의 제목은 체온이고 제목을 가운데 정렬함.
        treelist=[("2020-05-04 12:57:12", 36.5), ("2020-05-04 12:15:38", 37.3), 
                    ("2020-05-04 11:45:17", 36.4), ("2020-05-04 11:05:10", 36.9), ("2020-05-04 10:30:10", 37.1),
                    ("2020-05-04 10:02:15", 36.2)]
        #treelist라는 list형태로 columns[one,two]에 각각 측정시간과 체온값을 담음
        for i in range(len(treelist)):
            treeview.insert('', 'end', text=i+1, values=treelist[i], iid=str(i)+"번")
        #treelist의 길이값만큼 i를 반복문으로 실행. 루트('') 항목의 end 위치에 iid값이 i인 i+1을 treelist의 i번째 value로 받아넣음 
        treeview.tag_bind("tag1", sequence="<<TreeviewSelect>>", callback=cheon)

        #스크롤바 추가 시작==========================================================
        scrollbar = ttk.Scrollbar(frame1, orient="vertical", command=treeview.yview)
        scrollbar.place(x=335, y=20, height=130)
        treeview.configure(yscrollcommand=scrollbar.set)
        #스크롤바 끝==========================================================

#그래프 출력===========================================================
        print()
        w = 360
        h = 200
        x = 30
        x_m = 30
        x_b = 10
        y = 170
        b_t = [36.5, 37.4, 36.4, 36.9, 37.1, 36.2]
        label9=tk.Label(frame1, text="그래프로 보기")
        label9.pack()
        canvas = Canvas(frame1, width=w, height=h, bg='white')
        canvas.pack()
        line=canvas.create_line(50, 10, 50, h-10, fill="black") #x축 좌표(첫번째점의 x위치, 첫번째점의 y위치, 두번째점의 x위치, 두번y위치)
        line=canvas.create_line(20, h-30, w, h-30, fill="black")
        line=canvas.create_line(20, 170*(0.7/3), w, 170*(0.7/3), fill="red")
        for i in range(len(b_t)) :
            x += x_m + x_b
            if b_t[i] >= 37.4 :
                temp = "red"
            else :
                temp = "yellow"
            polygon=canvas.create_polygon(x, 170*((38-b_t[i])/3), x+x_m, 170*((38-b_t[i])/3), x+x_m, h-30, x, h-30, fill=temp, outline="red")
```
- 표 형태로 나타내기 위한 treeview 및 그래프 도식화를 위해 line을 이용하여 막대그래프를 나타냄.
- 초기에는 DB를 활용하지 않았으므로, 직접 입력된 값을 나타내는 방식을 이용하였고,
  그래프도 4개의 Line을 이어 막대를 그리는 형태로 구현함.



### (5) 표정 정보 상세 화면
```python
#표정 시작===================================================================================
        frame2=tk.Frame(window)
        notebook.add(frame2, text="기분상태")
        label10=tk.Label(frame2, text="표정별 기분상태")
        label10.pack()

        frameface=Frame(frame2, background="white",relief="groove", bd=1)
        frameface.pack(side=RIGHT, fill=BOTH, expand=YES)
        frametime=Frame(frame2, background="gray",relief="groove", bd=1)
        frametime.pack(side=LEFT, fill=BOTH, expand=YES)
        detection_time_label = Label(frametime,text="2020-05-06 09:30", relief="groove", bd=2)
        detection_time_label.pack()    
        facephoto = PhotoImage(file = "face.png") 
        label11 = Label(frame2,image = facephoto ,width=100, height=100)
        label11.image = facephoto
        label11.pack(side=TOP)
        frame_of_face = Frame(frame2,relief="groove")
        frame_of_face.pack(side=LEFT)
        analysis_face = ['happyness: 40%','sadness:20%','depression:5%','violence: 0%']
        values = StringVar(value=analysis_face)
        listbox = Listbox(master=frameface, listvariable=values, height=6)
        listbox.pack(fill=BOTH)
```
- 얼굴을 인식하여 표정에 따른 감정 정도를 나타내고자 하였음.
- 얼굴 인식 및 감정분석 딥러닝이 필요한 기능으로 추후 구현하고자 함.


### (6) 관리자 접속 화면
```python
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

        def cam_close():
            cap.release()

        def evend_logout(event):
            print("성공")
            frame1.destroy()
            frame2.destroy()
            notebook.destroy()
            cam_close()
            Login(window)
        button2 = Button(frame1,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)

        frame2=tk.Frame(window)
        notebook.add(frame2, text="학생")
        label2=tk.Label(frame2, text="페이지2의 내용")
        label2.pack()
```
- 관리자모드로 접속 시 현재 로봇이 촬영중인 실시간 영상을 나타내도록 구현함.



### (7) 로그아웃 및 종료
```python
#로그아웃 함수 및 버튼 생성(user mode)=======================================
        def evend_logout(event):
            bottom_frame.destroy()
            top_frame.destroy()
            Login(window)
        button2 = Button(bottom_frame,text="로그아웃")
        button2.pack(side=BOTTOM)
        button2.bind('<Button-1>',evend_logout)
```
- 로그아웃 버튼을 누를 경우 생성되어 있는 모든 윈도우 화면을 종료시킴.