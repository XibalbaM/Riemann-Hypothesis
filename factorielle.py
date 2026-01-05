from manim import *
from common import *

class Factorielle(Scene):
    def construct(self):
        title = Text("Définition de la factorielle", font_size=72, color=Colors.text).shift(UP)
        subtitle = MathTex("n!=n*(n-1)!=1*2*...*n", font_size=36, color=Colors.text).next_to(title, DOWN)
        by = Tex("$\\mathbb{R}$ ? Ou encore $\\mathbb{C}$ ?", font_size=24, color=Colors.text).next_to(subtitle, DOWN)
        self.play(Write(title), run_time=Durations.animations)
        self.play(Write(VGroup(subtitle, by)), run_time=Durations.animations)
        self.wait(Durations.pauses)
        self.play(FadeOut(subtitle), FadeOut(by), run_time=Durations.animations)

        self.play(FadeOut(title), run_time=Durations.animations)

        definition_title = Text("Définition formelle", font_size=48, color=Colors.text).to_edge(UP)
        definition = MathTex("n! = \\int_0^\\infty x^n e^{-x} \\, dx", font_size=36, color=Colors.text).next_to(definition_title, DOWN)
        self.play(Write(definition_title), run_time=Durations.animations)
        self.play(Write(definition), run_time=Durations.animations)
        self.wait(Durations.pauses)
        self.play(FadeOut(definition_title), FadeOut(definition), run_time=Durations.animations)

        

