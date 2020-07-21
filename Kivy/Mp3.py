import pygame
from pygame import mixer
import os

class Mpmp3:
    def __init__(self):        
        Mpmp3.capture_list=os.listdir(r'C:\Users\w\todayex\movie')
        print(Mpmp3.capture_list)
        self.list = os.listdir(r'C:\Users\w\todayex\movie')
        Mpmp3.capture_list.sort()
        print(list)

if __name__=='__main__':
    Mpmp3()
