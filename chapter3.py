from manim import *
from common import *
import numpy as np
import mpmath

# Configure mpmath to be reasonably fast
mpmath.mp.dps = 15

class Part3_1_TrivialZeros(Scene):
    def construct(self):
        title_mobject = chapter_title(self, 3)
        cleanup = chapter_subtitle(self, 3, 1, title_mobject=title_mobject)

        # 1. Negative real axis focus
        plane = ComplexPlane(
            x_range=[-11, 2, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        )
        self.play(Create(plane))

        # 2. Magnitude plot near negative real axis
        # Use a smaller resolution for speed if needed, but 128x128 should be okay
        def zeta_func(z):
            return mpmath.zeta(z)

        mag_label = MathTex(r"|\zeta(s)|", color=BLACK).to_edge(UP, buff=1.2)
        mag_plot = get_continuous_image(zeta_func, x_range=[-11, 2], y_range=[-4, 4], res_x=128, res_y=128, v_max=2)
        
        self.play(Write(mag_label))
        self.play(FadeIn(mag_plot))
        self.wait(1)

        # 3. Highlight trivial zeros at -2, -4, -6, -8, -10
        zeros_pos = [(-2, 0), (-4, 0), (-6, 0), (-8, 0), (-10, 0)]
        dots = VGroup(*[Dot(plane.c2p(x, y), color=RED) for x, y in zeros_pos])
        labels = VGroup(*[MathTex(str(x), color=RED, font_size=24).next_to(plane.c2p(x, y), DOWN) for x, y in zeros_pos])

        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.2))
        self.play(Write(labels))
        self.wait(2)

        # 4. Functional equation hint
        formula = MathTex(
            r"\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)",
            color=BLACK, font_size=30
        ).to_edge(DOWN, buff=0.5).set_background_stroke(color=WHITE, width=2, opacity=1)
        
        sin_part = MathTex(r"\sin\left(\frac{\pi s}{2}\right) = 0 \text{ pour } s = -2, -4, \dots", color=RED, font_size=24).next_to(formula, UP)
        
        self.play(Write(formula))
        self.play(Write(sin_part))
        self.wait(3)

        self.play(FadeOut(plane), FadeOut(mag_plot), FadeOut(mag_label), FadeOut(dots), FadeOut(labels), FadeOut(formula), FadeOut(sin_part), cleanup)

class Part3_2_NonTrivialZeros(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 2)

        plane = ComplexPlane(
            x_range=[-1, 2, 1],
            y_range=[-5, 35, 5],
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).scale(0.8).shift(DOWN * 2)
        
        # 1. Critical Strip
        strip = Rectangle(
            width=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
            height=plane.c2p(0, 35)[1] - plane.c2p(0, -5)[1],
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(plane.c2p(0.5, 15))
        
        strip_label = Text("Bande critique (0 < Re(s) < 1)", font_size=24, color=BLUE_E).next_to(strip, RIGHT)

        self.play(Create(plane))
        self.play(FadeIn(strip), Write(strip_label))
        self.wait(1)

        # 2. Critical Line
        line = Line(plane.c2p(0.5, -5), plane.c2p(0.5, 35), color=RED, stroke_width=4)
        line_label = Text("Droite critique (Re(s) = 1/2)", font_size=24, color=RED).next_to(line, LEFT)
        
        self.play(Create(line), Write(line_label))
        self.wait(1)

        # 3. Non-trivial zeros (first few)
        # 1/2 + i * 14.13, 21.02, 25.01
        zeros_im = [14.1347, 21.0220, 25.0108, 30.4248, 32.9351]
        zeros_dots = VGroup(*[Dot(plane.c2p(0.5, im), color=BLACK, radius=0.06) for im in zeros_im])
        zeros_dots_conj = VGroup(*[Dot(plane.c2p(0.5, -im), color=GRAY, radius=0.04) for im in zeros_im if im < 5]) # just show some below

        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in zeros_dots], lag_ratio=0.3))
        self.wait(1)

        # 4. Symmetry demonstration
        # If s is a zero, 1-s is a zero
        z_sample = complex(0.5, 14.13)
        dot_s = Dot(plane.c2p(0.5, 14.13), color=PURPLE)
        label_s = MathTex("s", color=PURPLE).next_to(dot_s, RIGHT)
        
        self.play(Indicate(zeros_dots[0]))
        self.play(Create(dot_s), Write(label_s))
        
        # Mirroring to 1-s (here it's the same because Re=1/2, but let's show anyway)
        sym_text = MathTex(r"s \in \mathcal{Z} \implies 1-s, \bar{s}, 1-\bar{s} \in \mathcal{Z}", color=BLACK, font_size=30).to_edge(UP, buff=1.2)
        self.play(Write(sym_text))
        self.wait(2)

        self.play(FadeOut(plane), FadeOut(strip), FadeOut(strip_label), FadeOut(line), FadeOut(line_label), FadeOut(zeros_dots), FadeOut(dot_s), FadeOut(label_s), FadeOut(sym_text), cleanup)

class Part3_3_HistoricalAdvances(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 3)

        # Timeline of calculations
        timeline = NumberLine(
            x_range=[1850, 2030, 20],
            length=10,
            color=BLACK,
            include_numbers=True,
            font_size=20
        ).shift(DOWN)
        
        self.play(Create(timeline))

        events = [
            (1859, "Riemann", "Les 3 premiers zéros"),
            (1903, "Gram", "15 zéros"),
            (1914, "Hardy", "Infinité de zéros sur la droite"),
            (1979, "Brent", "7 millions de zéros"),
            (2004, "Gourdon", "10 billions (10^13) zéros"),
            (2020, "Platt & Trudgian", "12 billions de zéros")
        ]

        entries = VGroup()
        for year, author, desc in events:
            line = Line(timeline.n2p(year), timeline.n2p(year) + UP * 1.5, color=BLUE_E)
            txt = Text(f"{author}\n({year})", font_size=16, color=BLACK).next_to(line, UP)
            subtxt = Text(desc, font_size=14, color=GRAY).next_to(txt, UP, buff=0.1)
            entries.add(VGroup(line, txt, subtxt))

        self.play(LaggedStart(*[FadeIn(e, shift=UP) for e in entries], lag_ratio=0.5, run_time=5))
        self.wait(3)

        self.play(FadeOut(timeline), FadeOut(entries), cleanup)

class Part3_4_RiemannHypothesis(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 4)

        # Focus on the statement
        rh_box = SurroundingRectangle(Text("L'Hypothèse de Riemann", color=BLUE_E), buff=0.5, color=BLUE_E)
        rh_title = Text("L'Hypothèse de Riemann", color=BLUE_E).move_to(rh_box)
        
        self.play(Create(rh_box), Write(rh_title))
        self.play(rh_box.animate.to_edge(UP), rh_title.animate.to_edge(UP))
        
        statement = MathTex(
            r"\text{Toutes les racines non-triviales } s \text{ de } \zeta(s)",
            r"\text{ont une partie réelle } \text{Re}(s) = \frac{1}{2}",
            color=BLACK, font_size=36
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(statement))
        self.wait(2)

        # Visual reminder
        plane = ComplexPlane(x_range=[0, 1, 0.5], y_range=[0, 50, 10], axis_config={"color": BLACK}).scale(0.5).to_edge(RIGHT)
        line = Line(plane.c2p(0.5, 0), plane.c2p(0.5, 50), color=RED, stroke_width=2)
        
        dots = VGroup(*[Dot(plane.c2p(0.5, im), color=BLACK, radius=0.03) for im in [14.13, 21.02, 25.01, 30.42, 32.93, 37.58, 40.91, 43.32, 48.00]])
        
        self.play(FadeIn(plane), Create(line), FadeIn(dots))
        self.wait(3)

        self.play(FadeOut(rh_box), FadeOut(rh_title), FadeOut(statement), FadeOut(plane), FadeOut(line), FadeOut(dots), cleanup)

class Part3_5_MillenniumProblems(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 5)

        # Clay Mathematics Institute
        clay_text = Text("Clay Mathematics Institute", font_size=40, color=BLUE_E).shift(UP * 2)
        logo_rect = Square(side_length=2, color=BLUE_E).next_to(clay_text, DOWN)
        problem_text = Text("Problèmes du prix du millénaire", font_size=32, color=BLACK).next_to(logo_rect, DOWN)
        
        self.play(Write(clay_text), Create(logo_rect), Write(problem_text))
        self.wait(1)

        # The Prize
        prize = Text("1 000 000 $", font_size=72, gradient=(GOLD_A, GOLD_E)).shift(DOWN * 0.5)
        self.play(ReplacementTransform(logo_rect, prize), FadeOut(problem_text))
        self.play(prize.animate.scale(1.2), run_time=0.5, rate_func=there_and_back)
        self.wait(2)

        # Status
        status_text = Text("Toujours non résolu (2025)", font_size=24, color=RED).next_to(prize, DOWN, buff=0.5)
        self.play(Write(status_text))
        self.wait(2)

        # Transition to Chapter 4
        next_chap = Text("Chapitre 4: Conséquences", font_size=36, color=BLACK).to_edge(DOWN, buff=1)
        self.play(Write(next_chap))
        self.wait(2)

        self.play(FadeOut(clay_text), FadeOut(prize), FadeOut(status_text), FadeOut(next_chap), cleanup)
