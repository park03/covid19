import pygame
from pygame import mixer
import os
# file_list=os.listdir(r'C:\Users\w\todayex')
# file_list.sort() #list를 이름순으로 정렬합니다
# print(file_list)

capture_list=os.listdir(r'C:\Users\w\todayex')
capture_list.sort()
print(capture_list)
# print(capture_list[-1]) #마지막 정보를 가져옴
# sp=capture_list[-1].split('frame') #frame9.jpg에서 frame을 자름
#위의 결과:['', '9.jpg']
# getnum=int(sp[-1].split('.jpg')[0]) #9.jpg에서 9만 가져옴
#['9', ''] 여기서 첫번째 값을 int 로 변경한다
# print(getnum)


# class FuncMp3():   
#     def __init__(self):
#         self.path_dir =  os.path.realpath('.') + '\mp3' #mp3 root 위치 변수
#         FuncMp3.file_list = os.listdir(self.path_dir) #폴더내의 파일 list 생성
#         # FuncMp3.file_list.sort() #리스트내 이름정렬
#         mixer.init()#mixer init
        
    
#     #노래 재생
#     def song_play(self,path):   
#         '''
#         음악 재생
#         path = 음악경로
#         '''       
#         mixer.music.load(self.path_dir + path)#파일 load
#         mixer.music.play()#mp3 play
#     def song_stop(self):
#         mixer.music.stop()

# if __name__ == '__main__':
#     print('ahahahahahahhahahah')



