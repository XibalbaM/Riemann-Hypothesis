from manim import *
from common import Colors, Durations, chapter_title, chapter_subtitle, setup_complex_plane

class TrivialZeros(Scene):
    def construct(self):
        chapter_title(self, "Les zéros", 3)
        cleanup = chapter_subtitle(self, "Les zéros", "Zéros triviaux", 3, 1)
        
        plane = setup_complex_plane(x_range=[-10, 2], y_range=[-4, 4])
        self.play(Create(plane), run_time=Durations.animations)
        
        # Zeros at -2, -4, -6...
        zeros = [-2, -4, -6, -8]
        dots = VGroup()
        labels = VGroup()
        
        for z in zeros:
            dot = Dot(plane.n2p(z), color=RED)
            label = MathTex(str(z)).next_to(dot, DOWN)
            dots.add(dot)
            labels.add(label)
            
        text = Text("Zéros triviaux aux entiers pairs négatifs", font_size=32, color=Colors.text).to_edge(UP).add_background_rectangle()
        
        self.play(Write(text), run_time=Durations.animations)
        self.play(Create(dots), Write(labels), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(plane), FadeOut(dots), FadeOut(labels), FadeOut(text), run_time=Durations.animations)
        cleanup()

class NonTrivialZeros(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Les zéros", "Zéros non-triviaux", 3, 2)
        
        plane = setup_complex_plane(x_range=[-2, 4], y_range=[-2, 30]) # Y range high to see zeros? 
        # Actually standard plane is small, we need to shift or scale y
        # Let's visualize the Critical Strip first
        
        plane = ComplexPlane(x_range=[-2, 4], y_range=[-5, 30], y_length=7).add_coordinates()
        self.play(Create(plane), run_time=Durations.animations)
        
        # Critical Strip 0 < Re(s) < 1
        strip = Rectangle(width=1 * plane.get_x_unit_size(), height=8, color=YELLOW, fill_opacity=0.2).move_to(plane.n2p(0.5) + UP * 0.5) # Centered at 0.5?
        # Plane coords: 0.5 is center of strip. Width is 1.
        # Check alignment. n2p(0.5) gives x coordinate.
        # Height is arbitrary large
        
        strip_label = Text("Bande critique", font_size=24, color=YELLOW).next_to(strip, RIGHT, buff=1)
        
        self.play(FadeIn(strip), Write(strip_label), run_time=Durations.animations)
        
        # Critical Line Re(s) = 1/2
        line = Line(plane.n2p(0.5 + -5j), plane.n2p(0.5 + 30j), color=RED)
        line_label = Text("Ligne critique (1/2)", font_size=24, color=RED).next_to(line, UP)
        
        self.play(Create(line), Write(line_label), run_time=Durations.animations)
        
        # Zeros
        # First few zeros: 14.13, 21.02, 25.01
        zeros_im = [14.13, 21.02, 25.01]
        dots = VGroup()
        for y in zeros_im:
            dot = Dot(plane.n2p(0.5 + y*1j), color=BLUE)
            dots.add(dot)
            
        zeros_text = Text("Les zéros semblent tous alignés...", font_size=24, color=BLUE).to_edge(DOWN).add_background_rectangle()
        
        self.play(Create(dots), Write(zeros_text), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(plane), FadeOut(strip), FadeOut(strip_label), FadeOut(line), FadeOut(line_label), FadeOut(dots), FadeOut(zeros_text), run_time=Durations.animations)
        cleanup()

class HistoricalProgress(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Les zéros", "Avancées historiques", 3, 3)
        
        # Timeline
        timeline = NumberLine(x_range=[1850, 2025, 25], length=12, color=Colors.text).add_numbers()
        self.play(Create(timeline), run_time=Durations.animations)
        
        events = [
            (1859, "Riemann publishes paper"),
            (1914, "Hardy proves infinitely many zeros on line"),
            (2004, "Gourdon verifies 10^13 zeros"),
        ]
        
        for year, desc in events:
            dot = Dot(timeline.n2p(year), color=RED)
            label = Text(desc, font_size=18, color=Colors.text).next_to(dot, UP, buff=0.5)
            date_label = Text(str(year), font_size=18, color=GRAY).next_to(dot, DOWN)
            
            self.play(Create(dot), FadeIn(label), FadeIn(date_label), run_time=0.5)
            self.wait(0.5)
        
        self.wait(Durations.pauses)
        self.play(FadeOut(timeline), *[mob for mob in self.mobjects if isinstance(mob, (Dot, Text, NumberLine))], run_time=Durations.animations)
        cleanup()

class RiemannHypothesis(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Les zéros", "L'hypothèse de Riemann", 3, 4)
        
        # Statement
        statement_text = Text("Hypothèse de Riemann", font_size=48, color=BLUE)
        self.play(Write(statement_text), run_time=Durations.animations)
        self.play(statement_text.animate.to_edge(UP))
        
        content = MathTex(r"\text{Tous les zéros non-triviaux ont pour partie réelle } \frac{1}{2}", color=Colors.text)
        self.play(Write(content), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Millennium Problem
        millennium = Text("Problème du millénaire (Clay Institute)", font_size=36, color=GOLD).next_to(content, DOWN, buff=1)
        prize = Text("1 000 000 $", font_size=48, color=GREEN).next_to(millennium, DOWN)
        
        self.play(Write(millennium), run_time=Durations.animations)
        self.play(Write(prize), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(statement_text), FadeOut(content), FadeOut(millennium), FadeOut(prize), run_time=Durations.animations)
        cleanup()
