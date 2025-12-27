from manim import *
from common import *

class Test(Scene):
    def construct(self):
        chapter_title(self, "Teest Chaptr", 1)
        fade_out_subtitle = chapter_subtitle(self, "Test Subtitle", "This is a subtitle for testing", 1, 1)
        self.wait(2)
        fade_out_subtitle()