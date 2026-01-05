from manim import *
from common import *
import numpy as np
import mpmath

class Part4_1_PrimeNumberTheorem(Scene):
    def construct(self):
        title_mobject = chapter_title(self, 4)
        cleanup = chapter_subtitle(self, 4, 1, title_mobject=title_mobject)

        # 1. Define pi(x)
        pi_def = MathTex(r"\pi(x) = \text{nombre de nombres premiers} \le x", color=BLACK).shift(UP * 2)
        self.play(Write(pi_def))
        self.wait(1)

        # 2. Gauss / Legendre conjecture (PNT)
        pnt_text = Text("Théorème des nombres premiers (Hadamard & de la Vallée-Poussin, 1896)", font_size=24, color=BLACK).next_to(pi_def, DOWN, buff=0.5)
        pnt_formula = MathTex(r"\pi(x) \sim \frac{x}{\ln(x)}", color=BLACK).next_to(pnt_text, DOWN)
        
        self.play(Write(pnt_text), Write(pnt_formula))
        self.wait(2)

        # 3. Better approximation: Li(x)
        li_def = MathTex(r"Li(x) = \int_2^x \frac{dt}{\ln t}", color=BLACK).next_to(pnt_formula, DOWN, buff=0.75)
        better_approx = Text("Meilleure approximation :", font_size=24, color=BLACK).next_to(li_def, UP, aligned_edge=LEFT)
        
        self.play(Write(better_approx), Write(li_def))
        self.wait(2)

        # 4. Visualization
        self.play(
            FadeOut(pi_def), FadeOut(pnt_text), FadeOut(pnt_formula), 
            FadeOut(li_def), FadeOut(better_approx)
        )

        ax = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 30, 5],
            x_length=10,
            y_length=6,
            axis_config={"color": BLACK},
            tips=False
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")

        # Actual primes count up to 100
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        points = []
        count = 0
        for x in range(101):
            if x in primes:
                count += 1
            points.append(ax.c2p(x, count))
        
        pi_graph = VMobject(color=RED)
        pi_graph.set_points_as_corners(points)
        pi_label = MathTex(r"\pi(x)", color=RED).next_to(pi_graph, RIGHT, buff=0.5).shift(UP * 0.5)

        # x / ln(x)
        def func_pnt(x):
            if x <= 1: return 0
            return x / np.log(x)
        
        pnt_graph = ax.plot(func_pnt, x_range=[2, 100], color=BLUE)
        pnt_label = MathTex(r"\frac{x}{\ln x}", color=BLUE).next_to(pnt_graph, RIGHT, buff=0.5).shift(DOWN * 0.5)

        # Li(x)
        def func_li(x):
            if x <= 1: return 0
            return float(mpmath.li(x))
         
        li_graph = ax.plot(func_li, x_range=[2, 100], color=GREEN)
        li_label = MathTex(r"Li(x)", color=GREEN).next_to(li_graph, RIGHT, buff=0.5).shift(UP * 1.5)

        self.play(Create(ax), Write(labels))
        self.play(Create(pi_graph), Write(pi_label))
        self.wait(1)
        self.play(Create(pnt_graph), Write(pnt_label))
        self.wait(1)
        self.play(Create(li_graph), Write(li_label))
        self.wait(2)

        self.play(
            FadeOut(ax), FadeOut(labels), 
            FadeOut(pi_graph), FadeOut(pi_label),
            FadeOut(pnt_graph), FadeOut(pnt_label),
            FadeOut(li_graph), FadeOut(li_label),
            cleanup
        )

class Part4_2_RiemannPrimeCountingFunction(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 4, 2)

        # 1. Connection text
        intro_text = Text(
            "Riemann a connecté la distribution des nombres premiers\naux zéros de la fonction zêta.",
            font_size=32, color=BLACK, line_spacing=1.5
        ).shift(UP * 2)
        
        self.play(Write(intro_text))
        self.wait(2)

        # 2. Explicit Formula
        
        formula = MathTex(
            r"&\pi_0(x) = R(x) - \sum_{\rho} R(x^\rho)\\"+
            r"&\pi_0(x) = \pi(x) - 0.5 \text{ si x est un nombre premier, sinon } \pi_0(x) = \pi(x)\\"+
            r"&R(x)=\sum_{n=1}^{\infty} \frac{\mu(n)}n \text{Li}(x^{1/n})\\"+
            r"&\text{Ça donne aussi }|\pi(x)-li(x)|<\frac{1}{8\pi}\sqrt{x}\log(x),",
            color=BLACK, font_size=36
        )

        self.play(ReplacementTransform(intro_text, formula))
        self.wait(1)

        self.play(FadeOut(formula), cleanup)

class Part4_3_OtherConsequences(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 4, 3)

        # List of consequences
        consequences = [
            "Distribution fine des nombres premiers (écarts)",
            "Théorie analytique des nombres (fonctions L, etc.)",
            "Cryptographie (RSA, tests de primalité)",
            "Physique (Chaos quantique, matrice aléatoire)",
            "Idée de preuve pour l’hypothèse de Riemann généralisée",
            "Plein d’autres conséquences sur tout ce qui touche aux entiers",
            "Certains théorèmes ont pu être montrés par le principe du tier-exclus"
        ]

        # Use a similar list style to previous chapters
        cons_grp = VGroup()
        for i, text in enumerate(consequences):
            dot = Dot(color=BLACK)
            t = Text(text, font_size=28, color=BLACK).next_to(dot, RIGHT)
            line = VGroup(dot, t)
            cons_grp.add(line)
        
        cons_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.5)
        
        self.play(LaggedStart(*[Write(obj) for obj in cons_grp], lag_ratio=0.7, run_time=3))
        self.wait(3)

        self.play(FadeOut(cons_grp), cleanup)
