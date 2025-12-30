from common import HeatmapMobject
from manim import *
from common import *
import numpy as np
import mpmath

class Part2_1_FirstValues(Scene):
    def construct(self):
        # Title
        title_mobject = chapter_title(self, 2)
        cleanup = chapter_subtitle(self, 2, 1, title_mobject=title_mobject)
        
        # Euler and the Basel Problem
        title_basel = Text("Le problème de Bâle (1650)", font_size=36, color=BLACK).to_edge(UP, buff=1.5)
        question = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \,\,?", color=BLACK).next_to(title_basel, DOWN, buff=0.5)
        
        self.play(Write(title_basel), Write(question))
        self.wait(1)
        
        euler_name = Text("Leonhard Euler (1735)", font_size=24, color=BLUE_E).next_to(question, LEFT, buff=1.5)
        euler_image = ImageMobject("assets/euler").next_to(euler_name, DOWN, buff=0.5)

        self.play(Write(euler_name), FadeIn(euler_image))
        self.wait(1)
        
        answer = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6} \approx 1.645", color=BLACK).move_to(question)
        self.play(Transform(question, answer))
        self.wait(2)
        
        # Other values
        zeta_4 = MathTex(r"\zeta(4) = \frac{\pi^4}{90}", color=BLACK).next_to(question, DOWN, buff=0.5).align_to(question, LEFT)
        
        self.play(Write(zeta_4))
        self.wait(2)

        # Even values formula
        even_values = MathTex(r"\zeta(2n) = \frac{(-1)^{n+1} B_{2n} (2\pi)^{2n}}{2 (2n)!}", color=BLACK).next_to(zeta_4, RIGHT, buff=0.5).align_to(zeta_4, UP)
        self.play(Write(even_values))
        self.wait(2)

        # Odd values?
        zeta_3 = MathTex(r"\zeta(3) \approx 1.202", color=BLACK).next_to(zeta_4, DOWN, buff=0.5).align_to(zeta_4, LEFT) 
        mystery = Text("(Constante d'Apéry - Pas de formule simple connue)", font_size=20, color=GRAY).next_to(zeta_3, DOWN)
        
        self.play(Write(zeta_3), FadeIn(mystery))
        self.wait(2)
        
        self.play(FadeOut(title_basel), FadeOut(question), FadeOut(euler_name), FadeOut(euler_image),
                  FadeOut(answer), FadeOut(zeta_4), FadeOut(zeta_3), FadeOut(even_values), FadeOut(mystery))
        self.play(cleanup)

class Part2_2_TheSeries(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 2, 2)

        # Presentation of the series formula
        formula = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}", color=BLACK).scale(1.5)
        self.play(Write(formula))

        # Definition of s
        s_def = MathTex(r"s = \sigma + i t", color=BLUE_E).next_to(formula, DOWN, buff=0.7)
        
        self.play(Write(s_def))
        self.wait(1.5)
        
        # Graphical representation of the series
        self.play(
            formula.animate.scale(0.6).to_corner(UL),
            FadeOut(s_def)
        )
        
        # Complex Plane Setup
        plane = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).add_coordinates()
        
        # Manually color coordinates black
        for mob in plane.coordinate_labels:
            mob.set_color(BLACK)
            
        self.play(Create(plane))
        
        # Example value s = 1.2 + 1.5i : converges
        s_val = 1.2 + 1.5j
        val_text = MathTex(f"s = {s_val.real} + {s_val.imag}i", color=BLACK, font_size=32).next_to(formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        self.play(Write(val_text))
        
        # Summation animation
        current_sum = 0j
        prev_point = plane.c2p(0, 0)
        arrows = VGroup()
        
        # We perform the sum for first 20 terms
        for n in range(1, 100):
            term = 1 / (n ** s_val)
            current_sum += term
            new_point = plane.c2p(current_sum.real, current_sum.imag)
            
            arrow = Arrow(prev_point, new_point, buff=0, color=BLUE_E if n%2==0 else BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            arrows.add(arrow)
            prev_point = new_point

        # Animate arrows
        for i, arrow in enumerate(arrows):
            # Slow at first, then fast
            speed = 1.0 if i < 3 else 1/i
            self.play(GrowArrow(arrow), run_time=speed)
            
        self.wait(2)
        self.play(FadeOut(arrows))
        
        # Example value s = 0.5 + 0.5i : diverges
        s_val = 0.5 + 0.5j
        val_text_2 = MathTex(f"s = {s_val.real} + {s_val.imag}i", color=BLACK, font_size=32).next_to(formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        self.play(Transform(val_text, val_text_2))
        
        # Summation animation
        current_sum = 0j
        prev_point = plane.c2p(0, 0)
        arrows = VGroup()
        
        # We perform the sum for first 50 terms
        for n in range(1, 50):
            term = 1 / (n ** s_val)
            current_sum += term
            new_point = plane.c2p(current_sum.real, current_sum.imag)
            
            arrow = Arrow(prev_point, new_point, buff=0, color=BLUE_E if n%2==0 else BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            arrows.add(arrow)
            prev_point = new_point

        # Animate arrows
        for i, arrow in enumerate(arrows):
            # Slow at first, then fast
            speed = 1.0 if i < 3 else 1/i
            self.play(GrowArrow(arrow), run_time=speed)
            
        self.wait(2)
        self.play(FadeOut(arrows))

        # Last example : s = 1 + i
        s_val = 1 + 1j
        val_text_3 = MathTex(f"s = {s_val.real} + {s_val.imag}i", color=BLACK, font_size=32).next_to(formula, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        self.play(Transform(val_text, val_text_3))

        # Summation animation
        current_sum = 0j
        prev_point = plane.c2p(0, 0)
        arrows = VGroup()
        
        # We perform the sum for first 50 terms
        for n in range(1, 50):
            term = 1 / (n ** s_val)
            current_sum += term
            new_point = plane.c2p(current_sum.real, current_sum.imag)
            
            arrow = Arrow(prev_point, new_point, buff=0, color=BLUE_E if n%2==0 else BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            arrows.add(arrow)
            prev_point = new_point

        # Animate arrows
        for i, arrow in enumerate(arrows):
            # Slow at first, then fast
            speed = 1.0 if i < 3 else 1/i
            self.play(GrowArrow(arrow), run_time=speed)
            
        
        self.wait(2)
        self.play(FadeOut(arrows))

        self.play(
            FadeOut(val_text), FadeOut(formula), FadeOut(plane)
        )

        # Show heatmap were it converges
        plane_heatmap = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.2}
        ).add_coordinates().set_z_index(1)
        for mob in plane_heatmap.coordinate_labels:
            mob.set_color(BLACK).scale(0.4)
        self.add(plane_heatmap)
        
        heatmap = always_redraw(lambda: HeatmapMobject(lambda z: complex(mpmath.zeta(z)), x_range=[1, 5], y_range=[-4, 4], x_length=4, y_length=8, mode="log")).move_to(plane_heatmap.c2p(3, 0))
        self.add(heatmap)
        self.wait(2)
        self.remove(heatmap)
        self.play(cleanup)

class Part2_3_AnalyticContinuation(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 2, 3)
        
        # The issue: definition only valid for Re(s) > 1
        formula = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} n^{-s}", color=BLACK).to_edge(UP, buff=1)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Visualizing the domain on complex plane
        plane = ComplexPlane(
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        )
        
        self.play(Create(plane))
        
        # Highlight Re(s) > 1
        # Create a rectangle covering Re(s) > 1
        # For visible area approx x in [-7, 7], y in [-4, 4]
        # We want x > 1
        
        valid_region = Polygon(
            plane.c2p(1, 10),
            plane.c2p(10, 10),
            plane.c2p(10, -10),
            plane.c2p(1, -10),
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0.3
        )
        
        label_valid = Text("Domaine de convergence initial", font_size=24, color=GREEN_E).move_to(plane.c2p(4, 2))
        
        self.play(FadeIn(valid_region), Write(label_valid))
        self.wait(2)
        
        # Continuation
        func_eq = MathTex(r"\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)", color=BLACK).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(func_eq))
        
        extended_region = Rectangle(
            width=20, height=20, fill_color=BLUE, fill_opacity=0.1, stroke_width=0
        )
        label_extended = Text("Défini partout (sauf s=1)", font_size=24, color=BLUE_E).to_edge(DOWN, buff=1)
        
        self.play(Transform(valid_region, extended_region), Transform(label_valid, label_extended))
        
        self.wait(3)
        
        self.play(
            FadeOut(plane), FadeOut(valid_region), FadeOut(func_eq),
            FadeOut(label_valid), FadeOut(formula)
        )
        
        # Euler Product
        title_product = Text("Produit d'Euler", font_size=36, color=BLACK).to_edge(UP, buff=1.5)
        
        # Formula
        # zeta(s) = product_{p prime} 1 / (1 - p^{-s})
        formula_product = MathTex(r"\zeta(s) = \prod_{p \text{ premiers}} \frac{1}{1 - p^{-s}}", color=BLACK).scale(1.2).next_to(title_product, DOWN, buff=1)
        
        self.play(Write(title_product), Write(formula_product))
        self.wait(2)
        
        explaination = Text("Même principe que le crible d'Eratosthène", font_size=24, color=BLACK).next_to(formula_product, DOWN, buff=0.5)
        
        self.play(Write(explaination))
        self.wait(2)
        
        self.play(
            FadeOut(title_product), FadeOut(formula_product), 
            FadeOut(explaination)
        )

        # Explicit definition via integral
        title_integral = Text("Définition explicite de Riemann", font_size=36, color=BLACK).to_edge(UP, buff=1.5)
        
        formula_integral = MathTex(r"\zeta(s) = \frac{1}{\Gamma(s)} \int_0^\infty \frac{x^{s-1}}{e^x - 1} \, dx", color=BLACK).next_to(title_integral, DOWN, buff=1)
        
        self.play(Write(title_integral), Write(formula_integral))
        self.wait(2)
        
        self.play(
            FadeOut(title_integral), FadeOut(formula_integral), cleanup
        )