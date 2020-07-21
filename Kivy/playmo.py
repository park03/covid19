import pygame
from pygame import mixer
import os
from kivy import event
from os.path import dirname

# from moviepy.editor import VideoFileClip
# from moviepy.editor import *



class FuncMp3():   
    def __init__(self):
        self.path_dir = f"{dirname(__file__)}/mp4/"  #mp3 root 위치 변수
        # print(self.path_dir)
        FuncMp3.file_list = os.listdir(self.path_dir) #폴더내의 파일 list 생성
        # print(FuncMp3.file_list)
        
        mixer.init()#mixer init
    
if __name__ == '__main__':
    # print('ahahahahahahhahahah')
    FuncMp3()
   

