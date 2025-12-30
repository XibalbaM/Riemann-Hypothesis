from manim import *
from common import *
import numpy as np

class Part2_1_ZetaFunction(Scene):
    def construct(self):
        # Title
        title_mobject = chapter_title(self, 2)
        cleanup = chapter_subtitle(self, 2, 1, title_mobject=title_mobject)

        # Definition
        # zeta(s) = sum_{n=1}^inf 1/n^s
        
        definition = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}", color=BLACK).scale(1.5)
        self.play(Write(definition))
        self.wait(1)
        
        # Move definition to top
        self.play(definition.animate.to_edge(UP, buff=1))
        
        # Test for s = 1 (Harmonic Series)
        s_val_1 = MathTex(r"s = 1", color=BLUE_E).next_to(definition, DOWN, buff=0.5)
        harmonic = MathTex(r"\zeta(1) = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \cdots", color=BLACK)
        diverges = Text("Diverge (vers l'infini)", color=RED, font_size=36).next_to(harmonic, DOWN, buff=0.5)
        
        self.play(Write(s_val_1))
        self.play(Write(harmonic))
        self.wait(1)
        self.play(FadeIn(diverges))
        self.wait(2)
        
        self.play(FadeOut(s_val_1), FadeOut(harmonic), FadeOut(diverges))
        
        # Test for s = 2
        s_val_2 = MathTex(r"s = 2", color=BLUE_E).next_to(definition, DOWN, buff=0.5)
        basel = MathTex(r"\zeta(2) = 1 + \frac{1}{4} + \frac{1}{9} + \frac{1}{16} + \cdots", color=BLACK)
        converges = Text("Converge", color=GREEN, font_size=36).next_to(basel, DOWN, buff=0.5)
        
        self.play(Write(s_val_2))
        self.play(Write(basel))
        self.wait(1)
        self.play(FadeIn(converges))
        self.wait(2)
        
        self.play(FadeOut(s_val_2), FadeOut(basel), FadeOut(converges), FadeOut(definition))
        self.play(cleanup)

class Part2_2_FirstValues(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 2, 2)
        
        # Euler and the Basel Problem
        title_basel = Text("Le problème de Bâle (1650)", font_size=36, color=BLACK).to_edge(UP, buff=1.5)
        question = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \,\,?", color=BLACK).next_to(title_basel, DOWN, buff=0.5)
        
        self.play(Write(title_basel), Write(question))
        self.wait(1)
        
        euler_image = Text("Leonhard Euler (1735)", font_size=24, color=BLUE_E).next_to(question, DOWN, buff=1)
        # Using text as placeholder for image/story
        
        self.play(FadeIn(euler_image))
        self.wait(1)
        
        answer = MathTex(r"= \frac{\pi^2}{6} \approx 1.645", color=GREEN_E).next_to(question, RIGHT)
        self.play(Write(answer))
        self.wait(2)
        
        # Other values
        zeta_4 = MathTex(r"\zeta(4) = \frac{\pi^4}{90}", color=BLACK).next_to(euler_image, DOWN, buff=1)
        zeta_6 = MathTex(r"\zeta(6) = \frac{\pi^6}{945}", color=BLACK).next_to(zeta_4, DOWN, buff=0.5)
        
        self.play(Write(zeta_4))
        self.play(Write(zeta_6))
        self.wait(2)
        
        # Odd values?
        zeta_3 = MathTex(r"\zeta(3) \approx 1.202", color=BLACK).next_to(zeta_6, DOWN, buff=0.5) 
        mystery = Text("(Constante d'Apéry - Pas de formule simple connue)", font_size=20, color=GRAY).next_to(zeta_3, RIGHT)
        
        self.play(Write(zeta_3), FadeIn(mystery))
        self.wait(2)
        
        self.play(FadeOut(title_basel), FadeOut(question), FadeOut(euler_image), 
                  FadeOut(answer), FadeOut(zeta_4), FadeOut(zeta_6), FadeOut(zeta_3), FadeOut(mystery))
        self.play(cleanup)

class Part2_3_AnalyticContinuation(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 2, 3)
        
        # The issue: definition only valid for Re(s) > 1
        formula = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} n^{-s}", color=BLACK).to_edge(UP, buff=1.5)
        condition = MathTex(r"\text{Converge pour } \text{Re}(s) > 1", color=RED).next_to(formula, DOWN)
        
        self.play(Write(formula), Write(condition))
        self.wait(1)
        
        # Visualizing the domain on complex plane
        plane = ComplexPlane(
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        ).scale(0.8).shift(DOWN*0.5)
        
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
        text_continuation = Text("Extension à tout le plan complexe", font_size=24, color=BLUE_E).to_edge(LEFT, buff=1).shift(UP)
        
        # Functional Equation
        # zeta(s) = 2^s pi^{s-1} sin(pi s / 2) Gamma(1-s) zeta(1-s)
        func_eq = MathTex(r"\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)", color=BLACK, font_size=32).to_edge(UP, buff=2.5)
        box = SurroundingRectangle(func_eq, color=BLUE_E, buff=0.1)
        
        self.play(FadeOut(valid_region), FadeOut(label_valid), FadeOut(condition))
        self.play(Write(text_continuation), Write(func_eq), Create(box))
        
        extended_region = Rectangle(
            width=20, height=20, fill_color=BLUE, fill_opacity=0.1, stroke_width=0
        )
        label_extended = Text("Défini partout (sauf s=1)", font_size=24, color=BLUE_E).move_to(plane.c2p(-2, 2))
        
        self.play(FadeIn(extended_region), Write(label_extended))
        
        # Pole at s=1
        pole = Dot(plane.c2p(1, 0), color=RED)
        label_pole = Text("Pôle simple en s=1", font_size=16, color=RED).next_to(pole, UP)
        
        self.play(Create(pole), Write(label_pole))
        self.wait(3)
        
        self.play(
            FadeOut(plane), FadeOut(extended_region), FadeOut(text_continuation), 
            FadeOut(func_eq), FadeOut(box), FadeOut(pole), FadeOut(label_pole),
            FadeOut(label_extended), FadeOut(formula)
        )
        self.play(cleanup)

class Part2_4_Definitions(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 2, 4)
        
        # Euler Product
        title_product = Text("Produit d'Euler", font_size=36, color=BLACK).to_edge(UP, buff=1.5)
        
        # Formula
        # zeta(s) = product_{p prime} 1 / (1 - p^{-s})
        formula_product = MathTex(r"\zeta(s) = \prod_{p \text{ premiers}} \frac{1}{1 - p^{-s}}", color=BLACK).scale(1.2).next_to(title_product, DOWN, buff=1)
        
        self.play(Write(title_product), Write(formula_product))
        self.wait(2)
        
        # Connection to primes
        connection_text = Text("Lien direct entre l'analyse et les nombres premiers", font_size=28, color=BLUE_E).next_to(formula_product, DOWN, buff=1)
        
        primes = MathTex(r"p \in \{2, 3, 5, 7, 11, 13, \dots\}", color=BLACK).next_to(connection_text, DOWN, buff=0.5)
        
        self.play(Write(connection_text))
        self.play(Write(primes))
        self.wait(3)
        
        # Maybe show the expansion for a few terms?
        # 1/(1-2^-s) * 1/(1-3^-s) ...
        # = (1 + 2^-s + 4^-s + ...) * (1 + 3^-s + 9^-s + ...) ...
        # = sum n^-s due to Unique Factorization Theorem
        
        expansion_idea = Text("Basé sur le Théorème Fondamental de l'Arithmétique", font_size=24, color=GRAY).to_edge(BOTTOM, buff=1)
        self.play(FadeIn(expansion_idea))
        self.wait(2)
        
        self.play(
            FadeOut(title_product), FadeOut(formula_product), 
            FadeOut(connection_text), FadeOut(primes), FadeOut(expansion_idea)
        )
        self.play(cleanup)
