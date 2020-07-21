
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App

from selectionbox import SelectionBox

Builder.load_file("imagepane.kv")


class ImagePane(Image):

    drawing_rectangle = None
    rectangles = []

    
    def __init__(self, **kwargs):
        super(ImagePane, self).__init__(**kwargs)
        self.register_event_type('on_store_rectangles')
    
    def on_store_rectangles(self, *args, **kwargs):
        pass

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            pos = [min(touch.pos[n], touch.opos[n]) for n in [0, 1]]
            size = [abs(touch.pos[n] - touch.opos[n]) for n in [0, 1]]
            if self.drawing_rectangle is None:
                self.drawing_rectangle = SelectionBox(pos=pos, size=size, image_pane=self)
                self.add_new_rectangle(self.drawing_rectangle)
            else:
                self.drawing_rectangle.pos = pos
                self.drawing_rectangle.size = size

    def on_touch_up(self, touch):
        if self.drawing_rectangle:
            self.drawing_rectangle.compute_unit_coordinates()
            self.drawing_rectangle = None
            self.store_rectangles()

    def add_new_rectangle(self, rect):
        self.add_widget(rect)
        self.rectangles.append(rect)
        
    def delete_last_rectangle(self):
        if self.rectangles:
            bad_rectangle = self.rectangles.pop()
            self.remove_widget(bad_rectangle)
            self.store_rectangles()
            
    def clear_rectangles(self):
        self.rectangles = []
        self.clear_widgets()

    def store_rectangles(self):
        self.dispatch('on_store_rectangles', rectangles=self.rectangles)

    def redraw_rectangles(self):
        for rect in self.rectangles:
            rect.compute_screen_coordinates()
