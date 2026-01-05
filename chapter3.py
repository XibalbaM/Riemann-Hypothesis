from common import HeatmapMobject
from manim import *
from common import *
import numpy as np
import mpmath

class Part3_1_TrivialZeros(Scene):
    def construct(self):
        title_mobject = chapter_title(self, 3)
        cleanup = chapter_subtitle(self, 3, 1, title_mobject=title_mobject)

        # 1. Negative real axis focus
        plane = ComplexPlane(
            x_range=[-11, 2, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).set_z_index(1)
        self.play(Create(plane))

        # 2. Magnitude plot near negative real axis
        def zeta_func(z):
            return complex(mpmath.zeta(z))

        mag_label = Text("|ζ(s)|", color=BLACK).to_edge(UP, buff=1.2)
        mag_plot = HeatmapMobject(zeta_func, x_range=[-11, 2], y_range=[-2, 2], x_length=13, y_length=4, mode="log")
        
        self.play(Write(mag_label))
        self.add(mag_plot)
        self.wait(1)

        # 3. Highlight trivial zeros at -2, -4, -6, -8, -10
        zeros_pos = [(-2, 0), (-4, 0), (-6, 0), (-8, 0), (-10, 0)]
        dots = VGroup(*[Dot(plane.c2p(x, y), color=RED) for x, y in zeros_pos])
        labels = VGroup(*[Text(str(x), color=BLACK, font_size=20).next_to(plane.c2p(x, y), DOWN) for x, y in zeros_pos])

        self.play(Create(dots))
        self.play(Write(labels))
        self.wait(2)

        # 4. Functional equation hint
        formula = MathTex(
            r'\zeta(s) = 2^s \pi^{s-1} \sin(\pi s/2) \Gamma(1-s) \zeta(1-s)',
            color=BLACK
        ).to_edge(DOWN, buff=0.5)
        
        
        self.play(Write(formula))
        self.wait(3)

        self.play(FadeOut(plane), FadeOut(mag_plot), FadeOut(mag_label), FadeOut(dots), FadeOut(labels), FadeOut(formula), cleanup)

class Part3_2_HistoricalAdvances(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 2)
        
        # 1. Symmetry
        # ----------------
        plane = ComplexPlane(
            x_range=[-4, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        )
        
        self.play(Create(plane))
        
        # S points
        s_val = complex(0.7, 2.5)
        names = ["s", r"\bar{s}", r"1-s", r"1-\bar{s}"]
        dirs = [UR, DR, DL, UL]
        
        # Helper to get points: s, conj(s), 1-s, 1-conj(s)
        points_c = [s_val, np.conj(s_val), 1 - s_val, 1 - np.conj(s_val)]
        
        dots = VGroup()
        labels = VGroup()
        
        for p, name, d in zip(points_c, names, dirs):
            dot = Dot(plane.n2p(p), color=RED)
            lbl = MathTex(name, color=BLACK).next_to(dot, d, buff=0.1)
            dots.add(dot)
            labels.add(lbl)
            
        # Critical line for symmetry reference (Re(s)=1/2)
        crit_line = DashedLine(
            plane.n2p(0.5 - 5j), 
            plane.n2p(0.5 + 5j), 
            color=BLUE
        )
        crit_label = MathTex("Re(s)=1/2", color=BLUE, font_size=24).next_to(crit_line, UP)
        
        self.play(Create(dots[0]), Write(labels[0]))
        self.play(Create(crit_line), Write(crit_label))
        
        # Animate symmetries
        # Functional Symmetery: s <-> 1-s
        self.play(TransformFromCopy(dots[0], dots[2]), TransformFromCopy(labels[0], labels[2]))
        
        # Conjugate Symmetery: s <-> bar(s)
        self.play(TransformFromCopy(dots[0], dots[1]), TransformFromCopy(labels[0], labels[1]))
        
        # Complete rectangle
        self.play(TransformFromCopy(dots[2], dots[3]), TransformFromCopy(labels[2], labels[3]))
        
        self.wait(1)
       
        functional_equation = MathTex(
            r'\zeta(s) = 2^s \pi^{s-1} \sin(\pi s/2) \Gamma(1-s) \zeta(1-s)',
            color=BLACK
        )
        
        self.play(Write(functional_equation))
        self.wait(2)
        
        # 2. Critical Strip
        # ----------------
        self.play(FadeOut(dots), FadeOut(labels), FadeOut(functional_equation))
        
        strip = Rectangle(
            width=plane.x_axis.unit_size * 1,
            height=plane.y_axis.unit_size * 10,
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to(plane.n2p(0.5)) 
        
        strip_label = Text("Bande Critique", font_size=32, color=BLACK).next_to(strip, UP, buff=0.1)
        strip_label.set_z_index(2)
        
        self.play(FadeIn(strip), Write(strip_label))
        
        # Constraints text
        constraint_1 = MathTex(r"\zeta(s) \neq 0 \text{ si } Re(s) \ge 1", color=BLACK, font_size=36).to_corner(UL).shift(DOWN)
        constraint_2 = Text("Hadamard & de la Vallée-Poussin (1896)", font_size=24, color=BLACK).next_to(constraint_1, DOWN, aligned_edge=LEFT)
        constraint_3 = MathTex(r"\zeta(s) \neq 0 \text{ si } Re(s) = 1", color=BLACK, font_size=36).next_to(constraint_2, DOWN, aligned_edge=LEFT)

        self.play(Write(constraint_1))
        self.wait(1)
        self.play(Write(constraint_2), Write(constraint_3))
        self.wait(2)
        
        # 3. First Computed Zeros
        # ----------------
        self.play(
            FadeOut(constraint_1), 
            FadeOut(constraint_2), 
            FadeOut(constraint_3),
            FadeOut(strip_label),
            FadeOut(strip), 
            FadeOut(plane),
            FadeOut(crit_line),
            FadeOut(crit_label)
        )
        
        # New Plane for Zeros (zoomed out y-axis)
        plane_zeros = ComplexPlane(
            x_range=[-2, 6, 1], 
            y_range=[-2, 32, 5],
            x_length=6, 
            y_length=7,
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).shift(DOWN * 0.5) 
        
        new_crit_line = Line(plane_zeros.n2p(0.5 - 2j), plane_zeros.n2p(0.5 + 32j), color=BLUE, stroke_width=2)
        
        new_strip = Rectangle(
             width=plane_zeros.x_axis.unit_size * 1,
             height=plane_zeros.y_axis.unit_size * 34,
             fill_color=YELLOW,
             fill_opacity=0.3,
             stroke_width=0
        ).move_to(plane_zeros.n2p(0.5 + 15j))

        self.play(FadeIn(plane_zeros), FadeIn(new_strip), Create(new_crit_line))
        
        valid_zeros = [14.13, 21.02, 25.01]
        zero_grp = VGroup()
        
        for im in valid_zeros:
            z_pt = plane_zeros.n2p(0.5 + im * 1j)
            d = Dot(z_pt, color=RED)
            l = MathTex(f"1/2 + {im}i", font_size=24, color=RED).next_to(d, RIGHT)
            zero_grp.add(d, l)
            
        self.play(LaggedStart(*[Write(obj) for obj in zero_grp], lag_ratio=0.2, run_time=2))
        
        self.wait(2)
        
        self.play(
            FadeOut(plane_zeros), FadeOut(new_strip), FadeOut(new_crit_line),   
            FadeOut(zero_grp),
            cleanup
        )

class Part3_3_RiemannHypothesis(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 3)

        # 1. Critical Line
        plane = ComplexPlane(
            x_range=[-2, 4, 1],
            y_range=[-2, 30, 5],
            x_length=6,
            y_length=7,
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).shift(LEFT * 2)

        crit_line = Line(
            plane.n2p(0.5 - 2j),
            plane.n2p(0.5 + 30j),
            color=BLUE,
            stroke_width=4
        )
        
        self.play(Create(plane), Create(crit_line))
        
        # Show some zeros on the line (schematic)
        # 14.13, 21.02, 25.01
        zeros_y = [14.13, 21.02, 25.01]
        zeros_dots = VGroup()
        for y in zeros_y:
            dot = Dot(plane.n2p(0.5 + y*1j), color=RED)
            zeros_dots.add(dot)
            
        self.play(Create(zeros_dots))
        self.wait(1)

        # 2. The statement
        statement_text = Tex(
            r"Tous les zéros non triviaux\\",
            r"de la fonction $\zeta(s)$ ont pour\\",
            r"partie réelle $Re(s) = \frac{1}{2}$",
            color=BLACK, font_size=34
        )

        self.play(Write(statement_text))
        self.play(Circumscribe(statement_text))
        self.wait(2)

        self.play(FadeOut(statement_text), FadeOut(zeros_dots), FadeOut(plane), FadeOut(crit_line))
        # 3. Evidences
        evidences = [
            "Testé jusqu'à 3 × 10¹²", 
            "Il y a une infinité de zéros sur la ligne critique (Hardy & Littlewood)", 
            "Selberg (1942) : La proportion des zéros sur la ligne critique n’est pas nulle",
            "Levinson (1974) : Elle est supérieure à 1/3",
            "Conrey (1989) : Elle est supérieure à 2/5",
            "Pratt, Robles, Zaharescu et Zeindler (2020) : Elle est supérieure à 5/12"
        ]

        evidences_grp = VGroup()
        for i, text in enumerate(evidences):
            t = Text(text, font_size=24, color=BLACK).next_to(statement_text, DOWN, buff=0.5)
            evidences_grp.add(t)
        evidences_grp.arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(evidences_grp))
        self.wait(2)

        self.play(FadeOut(evidences_grp))
        self.wait(2)

        self.play(cleanup)

class Part3_4_MillenniumProblems(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 3, 4)

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
        self.play(FadeOut(prize))

        # List of intitulates
        intitulates = [
            "Conjecture de Poincaré",
            "Conjecture de Birch et Swinnerton-Dyer",
            "Conjecture de Hodge",
            "Conjecture de Riemann",
            "Existence de théorie de Yang-Mills",
            "Équation de Navier-Stokes",
            "P vs NP"
        ]

        intitulates_grp = VGroup()
        for i, text in enumerate(intitulates):
            t = Text(text, font_size=24, color=BLACK).next_to(prize, DOWN, buff=0.5)
            intitulates_grp.add(t)
        intitulates_grp.arrange(DOWN, aligned_edge=LEFT)
        intitulates_grp.next_to(clay_text, DOWN, buff=0.5)
        self.play(LaggedStart(*[Write(obj) for obj in intitulates_grp], lag_ratio=0.2, run_time=2))
        self.wait(2)

        self.play(FadeOut(intitulates_grp), FadeOut(clay_text), cleanup)