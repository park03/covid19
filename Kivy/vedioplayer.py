from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.behaviors.focus import FocusBehavior
import pygame
from pygame import mixer
import os
from Mp3 import * 

Builder.load_string('''
<RV>:
    viewclass: 'Button'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        # Button:    
        #     on_press: print("sdfs")
            
''')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.mp = Mpmp3()
        self.list__ = Mpmp3.capture_list
        # print(self.list__)
        self.data = [{'text': str(x)} for x in self.list__]
    
    


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()



####################################
class Rvs(RecycleView):
    def __init__(self, **kwargs):
        super(Rvs, self).__init__(**kwargs)
        list_ = ListProperty([])
        list_ = mp3.FuncMp3.file_list
        # self.data = [{'text':str(i)} for i in fm.Func_Class.file_list]#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)
        for item in list_:
            self.data.append({'text':str(item),'font_name':'HANDotum'} )#data 를 만들 때 튜플 형식으로 만들어야 한다.(key:vlaue)
##
####################셀렉트 만들기########################
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):# 셀렉트 리스트 화면 구성
    ''' Adds selection and focus behaviour to the view. '''

##
class SelectableLabel(RecycleDataViewBehavior, Label):#셀렉트 리스트가 동작 하는것을 감지 하는 클래스
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    def refresh_view_attrs(self, rvs, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rvs, index, data)
    
    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rvs, index, is_selected):
        ''' Respond to the selection of items in the view. '''        
        self.selected = is_selected
        if is_selected:
            
            print("selection changed to {0}".format(rvs.data[index]))
        else:
            print("selection removed for {0}".format(rvs.data[index]))
#########################################################
