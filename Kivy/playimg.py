import pygame
from pygame import mixer
import os
from kivy import event
from os.path import dirname


class FuncImg():   
    def __init__(self):
        self.path_dir = f"{dirname(__file__)}/draw/"  
        # print(self.path_dir)
        FuncImg.file_list = os.listdir(self.path_dir) #폴더내의 파일 list 생성
        # print(FuncImg.file_list)
        
        # mixer.init()#mixer init


    
if __name__ == '__main__':
    # print('ahahahahahahhahahah')
    FuncImg()