
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file('selectionbox.kv')


class SelectionBox(Widget):

    def __init__(self, image_pane, text='', pos=None, size=None, unit_pos=None, unit_size=None):
        super(SelectionBox, self).__init__(pos=pos, size=size)
        self.label.text = text
        self.image_pane = image_pane
        self.unit_pos = unit_pos
        self.unit_size = unit_size
        
    def to_dict(self):
        return {'text': self.label.text, 'pos': self.pos, 'size': self.size,
                'unit_pos': self.unit_pos, 'unit_size': self.unit_size}

    def compute_unit_coordinates(self):
        image_pos = [self.image_pane.pos[n] + (self.image_pane.size[n] - self.image_pane.norm_image_size[n]) / 2
                     for n in (0, 1)]
        self.unit_pos = tuple([(self.pos[n] - image_pos[n]) * 1.0 / self.image_pane.norm_image_size[n] for n in [0, 1]])
        self.unit_size = tuple([self.size[n] * 1.0 / self.image_pane.norm_image_size[n] for n in [0, 1]])

    def compute_screen_coordinates(self, *_):
        image_pos = [self.image_pane.pos[n] + (self.image_pane.size[n] - self.image_pane.norm_image_size[n]) / 2
                     for n in (0, 1)]
        self.pos = [self.unit_pos[n] * self.image_pane.norm_image_size[n] + image_pos[n] for n in [0, 1]]
        self.size = [self.unit_size[n] * self.image_pane.norm_image_size[n] for n in [0, 1]]

        
