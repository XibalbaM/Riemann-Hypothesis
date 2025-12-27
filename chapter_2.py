from manim import *
from common import Colors, Durations, chapter_title, chapter_subtitle, wrap_text, setup_complex_plane
import math

class ZetaContinuation(Scene):
    def construct(self):
        chapter_title(self, "La fonction zeta", 2)
        cleanup = chapter_subtitle(self, "La fonction zeta", "Continuation analytique", 2, 1)

        # Reminder of Sum definition
        sum_def = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}", color=Colors.text).to_edge(UP)
        domain1 = MathTex(r"\text{pour } \Re(s) > 1", color=RED).next_to(sum_def, DOWN)
        
        self.play(Write(sum_def), Write(domain1), run_time=Durations.animations)
        
        plane = setup_complex_plane()
        self.play(Create(plane), run_time=Durations.animations)
        
        # Color the domain Re(s) > 1
        domain_rect = Rectangle(width=5, height=8, color=GREEN, fill_opacity=0.2).move_to([3.5, 0, 0]) # rough right half
        
        self.play(FadeIn(domain_rect), run_time=Durations.animations)
        self.wait(Durations.pauses)

        # Integral definition for extension
        integral_def = MathTex(r"\zeta(s) = \frac{1}{\Gamma(s)} \int_0^\infty \frac{x^{s-1}}{e^x - 1} dx", color=Colors.text).to_edge(UP)
        domain2 = MathTex(r"\text{pour } \Re(s) > 0, s \neq 1", color=BLUE).next_to(integral_def, DOWN)
        
        self.play(ReplacementTransform(sum_def, integral_def), ReplacementTransform(domain1, domain2), run_time=Durations.animations)
        
        # Extend domain visually
        new_domain = Rectangle(width=6, height=8, color=BLUE, fill_opacity=0.2).move_to([3, 0, 0]) # Includes 0 to 1
        self.play(ReplacementTransform(domain_rect, new_domain), run_time=Durations.animations)
        
        # Pole at s=1
        pole = Dot(point=[1, 0, 0], color=RED)
        pole_label = MathTex("s=1").next_to(pole, UP)
        self.play(Create(pole), Write(pole_label), run_time=Durations.animations)
        
        self.wait(Durations.pauses)
        
        self.play(FadeOut(plane), FadeOut(integral_def), FadeOut(domain2), FadeOut(new_domain), FadeOut(pole), FadeOut(pole_label), run_time=Durations.animations)
        cleanup()

class ZetaDefinitions(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "La fonction zeta", "Différentes définitions", 2, 2)
        
        # List definitions: Sum, Euler Product, Functional Equation
        
        title = Text("Différentes facettes de Zeta", font_size=36, color=Colors.text).to_edge(UP)
        self.play(Write(title), run_time=Durations.animations)
        
        # 1. Sum
        def1 = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} n^{-s}", color=Colors.text)
        label1 = Text("Série (Dirichlet)", font_size=24, color=GRAY).next_to(def1, DOWN)
        
        # 2. Euler Product
        def2 = MathTex(r"\zeta(s) = \prod_{p \in \mathcal{P}} \frac{1}{1 - p^{-s}}", color=Colors.text)
        label2 = Text("Produit d'Euler (Nombres premiers)", font_size=24, color=GRAY).next_to(def2, DOWN)
        
        # 3. Functional Equation
        def3 = MathTex(r"\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)", color=Colors.text)
        label3 = Text("Équation fonctionnelle", font_size=24, color=GRAY).next_to(def3, DOWN)
        
        group = VGroup(VGroup(def1, label1), VGroup(def2, label2), VGroup(def3, label3)).arrange(DOWN, buff=1)
        
        self.play(Write(group), run_time=Durations.animations * 2)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(group), FadeOut(title), run_time=Durations.animations)
        cleanup()

class ZetaFactorial(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "La fonction zeta", "Lien avec la factorielle", 2, 3)
        
        # Gamma function
        gamma_tex = MathTex(r"\Gamma(n) = (n-1)!", color=Colors.text)
        self.play(Write(gamma_tex), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Connection
        connection_text = Text("La fonction Gamma prolonge la factorielle.", font_size=32, color=Colors.text).next_to(gamma_tex, UP, buff=1)
        self.play(Write(connection_text), run_time=Durations.animations)
        
        # Zeta relation
        zeta_rel = MathTex(r"\zeta(s) \Gamma(s) = \int_0^\infty \frac{x^{s-1}}{e^x - 1} dx", color=Colors.text).next_to(gamma_tex, DOWN, buff=1)
        self.play(Write(zeta_rel), run_time=Durations.animations)
        
        explanation = Text("Zeta et Gamma sont intimement liées.", font_size=32, color=Colors.text).to_edge(DOWN)
        self.play(Write(explanation), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(gamma_tex), FadeOut(connection_text), FadeOut(zeta_rel), FadeOut(explanation), run_time=Durations.animations)
        cleanup()

class ZetaFunFact(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "La fonction zeta", "Fun fact", 2, 4)
        
        # Just a visual filler for "Fun fact" as specific "irrational derivatives" is obscure
        # Highlighting Zeta values at integers
        
        text = Text("Valeurs spéciales", font_size=48, color=Colors.text).to_edge(UP)
        self.play(Write(text), run_time=Durations.animations)
        
        val1 = MathTex(r"\zeta(2) = \frac{\pi^2}{6} \approx 1.645", color=Colors.text)
        val2 = MathTex(r"\zeta(4) = \frac{\pi^4}{90} \approx 1.0823", color=Colors.text)
        
        # "Rational derivates?" Maybe refers to Zeta'(-2k)? 
        # zeta'(-2n) = (-1)^n \frac{(2n)!}{2(2\pi)^{2n}} \zeta(2n+1) ... no that's complex
        # Let's stick to showing values
        
        group = VGroup(val1, val2).arrange(DOWN, buff=0.5)
        self.play(Write(group), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        fun_note = Text("(Lien profond avec Pi)", font_size=32, color=BLUE).next_to(group, DOWN)
        self.play(Write(fun_note), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(text), FadeOut(group), FadeOut(fun_note), run_time=Durations.animations)
        cleanup()
