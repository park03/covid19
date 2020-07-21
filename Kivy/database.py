import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            username, password, parentname, childrenname, signup, login = line.strip().split(";")
            self.users[username] = (password, parentname, childrenname, signup, login)
       
        self.file.close()

    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        else:
            return -1

    def add_user(self, username ,password, parentname, childrenname):
        if username.strip() not in self.users:
            self.users[username.strip()] = (password.strip(), parentname.strip(), childrenname.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            invalidForm()
            return -1

    def validate(self, username, password):
        if self.get_user(username) != -1:
            return self.users[username][0] == password
        else:
            return invalidLogin()

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1]+ ";" + self.users[user][2]+ ";"+ self.users[user][3]+ ";"+"\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
def invalidLogin():
    pop = Popup( title= "로그인" ,
                 content=Label(text='아이디/비밀번호 확인하세요'),
                  size_hint=(None, None), size=(300, 100),  background = 'popup.png')
    pop.open()

def invalidForm():
    
    pop = Popup(title= "회원가입" ,
                 content=Label(text='등록된 아이디 입니다.'),
                  size_hint=(None, None), size=(300, 100),  background = 'popup1.png')
    pop.open()