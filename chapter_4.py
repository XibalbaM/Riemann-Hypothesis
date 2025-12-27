from manim import *
from common import Colors, Durations, chapter_title, chapter_subtitle
import math

class PrimeNumberTheorem(Scene):
    def construct(self):
        chapter_title(self, "Conséquences", 4)
        cleanup = chapter_subtitle(self, "Conséquences", "Distribution des nombres premiers", 4, 1)
        
        # PNT Statement
        title = Text("Théorème des nombres premiers", font_size=36, color=Colors.text).to_edge(UP)
        self.play(Write(title), run_time=Durations.animations)
        
        pi_x = MathTex(r"\pi(x) \sim \frac{x}{\ln(x)}", color=Colors.text)
        self.play(Write(pi_x), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Connection to RH
        rh_implication = Text("L'Hypothèse de Riemann donne la meilleure borne d'erreur.", font_size=24, color=Colors.text).next_to(pi_x, DOWN, buff=1)
        error_term = MathTex(r"|\pi(x) - \text{Li}(x)| < \frac{1}{8\pi} \sqrt{x} \ln(x)", color=Colors.text).next_to(rh_implication, DOWN)
        
        self.play(Write(rh_implication), Write(error_term), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(title), FadeOut(pi_x), FadeOut(rh_implication), FadeOut(error_term), run_time=Durations.animations)
        cleanup()

class OtherConsequences(Scene):
    def construct(self):
        # Specific sub-chapter for other theorems
        # No formal subtitle needed, just a list
        
        list_obj = BulletedList(
            "Test de primalité de Miller-Rabin (Version déterministe)",
            "Espacement entre les nombres premiers",
            "Fonctions L de Dirichlet",
            font_size=24, color=Colors.text
        )
        
        self.play(Write(list_obj), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        final_text = Text("C'est la clé de voûte de la théorie des nombres.", font_size=32, color=BLUE).to_edge(DOWN)
        self.play(Write(final_text), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(list_obj), FadeOut(final_text), run_time=Durations.animations)
