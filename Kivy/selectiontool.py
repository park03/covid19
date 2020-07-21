
import os
import glob
import json
from os.path import dirname

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App
import kivy 

from imagepane import ImagePane
from selectionbox import SelectionBox
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
resource_add_path('c:/windows/fonts')
LabelBase.register(DEFAULT_FONT, 'H2GTRE.TTF')

from kivy.lang import Builder
with open(f"{dirname(__file__)}/selectiontool.kv", encoding='utf-8') as f: # Note the name of the .kv 
    Builder.load_string(f.read())
import time
from datetime import datetime
from os.path import dirname


# Builder.load_file('selectiontool.kv')


class SelectionTool(BoxLayout):
    library_directory = f"{dirname(__file__)}/Example_Data"
    book_id = StringProperty()
    page = StringProperty()
    
    def Ss(self): 
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.export_to_png(f"{dirname(__file__)}\word\IMG_"+timestr+".png")
        # print(timestr)

    def __init__(self):
        super(SelectionTool, self).__init__()
        self.image_pane.bind(on_store_rectangles=self.store_rectangles)
        self.all_rectangles = {}
        self.rectangles_filename = 'rectangles.json'
        self.load_rectangles()
        
        book_pattern = os.path.join(self.library_directory, '[0-9]' * 4)
        self.book_selector.values = [os.path.basename(s) for s in glob.glob(book_pattern)]
        self.book_selector.text = self.book_selector.values[0] if self.book_selector.values else 'No Books'

        self.on_book_id()
        
    def on_book_id(self, inst=None, value=None):
        image_pattern = os.path.join(self.library_directory, self.book_id, '*.jpg')
        self.page_selector.values = [os.path.basename(s)[:-4] for s in glob.glob(image_pattern)]
        self.page_selector.text = self.page_selector.values[0] if self.page_selector.values else 'No Images'
        
        # self.word_list.clear_widgets()
        # with open(os.path.join(self.library_directory, self.book_id, 'word_list.txt')) as fp:
        #     for word in sorted(fp.readlines()):
        #         self.word_list.add_widget(Label(text=word.strip()))
        # self.color_word_list()
        
        self.on_page()
    
    def on_page(self, *_):
        page_filename = self.page + '.jpg'
        self.image_pane.source = os.path.join(self.library_directory, self.book_id, page_filename)
        self.image_pane.clear_rectangles()
        try:
            for rect in self.all_rectangles[self.book_id][self.page]:
                rect.compute_screen_coordinates()
                self.image_pane.add_new_rectangle(rect)
        except KeyError:
            pass
        
    def store_rectangles(self, sender=None, rectangles=[]):
        if self.book_id not in self.all_rectangles:
            self.all_rectangles[self.book_id] = {}
        self.all_rectangles[self.book_id].update({self.page: [r for r in rectangles]})
        self.color_word_list()
        self.save_rectangles()

    def load_rectangles(self):
        self.all_rectangles = {}
        try:
            with open(self.rectangles_filename) as fd:
                all_rectangles_dict = json.load(fd)
                for book_id, book_rectangles in all_rectangles_dict.items():
                    self.all_rectangles[book_id] = {}
                    for page, rectangles in book_rectangles.items():
                        self.all_rectangles[book_id][page] = \
                            [SelectionBox(image_pane=self.image_pane, **rect) for rect in rectangles]
        except IOError:
            print("Can't find rectangles file!")
        
    def save_rectangles(self):
        rectangle_dict = {}
        for book_id, book_rectangles in self.all_rectangles.items():
            for page, rectangles in book_rectangles.items():
                page_dict = {page: [rect.to_dict() for rect in rectangles]}
                if rectangles:
                    rectangle_dict[book_id] = rectangle_dict.get(book_id, {})
                    rectangle_dict[book_id].update(page_dict)
        
        with open(self.rectangles_filename, 'w') as fd:
            json.dump(rectangle_dict, fd, sort_keys=True, indent=4, separators=(',', ': '))
     
    def color_word_list(self):
        if self.book_id in self.all_rectangles:
            rectangle_labels = [rect.label.text for page_rects in self.all_rectangles[self.book_id].values()
                                for rect in page_rects]
        else:
            rectangle_labels = []
            
        # for label in self.word_list.children:
        #     label.color = (0, 1, 0, 1) if label.text in rectangle_labels else (1, 1, 1, 1)

    def __init__(self):
        super(SelectionTool, self).__init__()
        self.image_pane.bind(on_store_rectangles=self.store_rectangles)
        self.all_rectangles = {}
        if kivy.platform == 'ios': # added
            self.rectangles_filename = os.path.join(App.get_running_app().user_data_dir, 'rectangles.json')
        else:
            self.rectangles_filename = 'rectangles.json'
        self.load_rectangles()
        
        book_pattern = os.path.join(self.library_directory, '[0-9]' * 4)
        self.book_selector.values = [os.path.basename(s) for s in glob.glob(book_pattern)]
        self.book_selector.text = self.book_selector.values[0] if self.book_selector.values else 'No Books'
