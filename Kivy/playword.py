import pygame
from pygame import mixer
import os
from kivy import event
from os.path import dirname


class FuncWord():   
    def __init__(self):
        self.path_dir = f"{dirname(__file__)}/word/"  
        # print(self.path_dir)
        FuncWord.file_list = os.listdir(self.path_dir) #폴더내의 파일 list 생성
        # print(FuncWord.file_list)
        
        # mixer.init()#mixer init


    
if __name__ == '__main__':
    # print('ahahahahahahhahahah')
    FuncWord()