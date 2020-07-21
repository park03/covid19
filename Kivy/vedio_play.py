from kivy.app import App
from kivy.uix.videoplayer import VideoPlayer


class TestApp(App):
    vid = None

    def replay(self, instance, value):
        if value != "play":
            # self.vid.play = True
            self.vid.state = "play"

    def build(self):
        self.vid = VideoPlayer(source="./zz1104-1000-.mp4", state="play")
        # self.vid.bind(state=self.replay)  # When state changes, if not playing, play it
        return self.vid


TestApp().run()