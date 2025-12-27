from manim import *
from common import Colors, Durations, chapter_title, chapter_subtitle, wrap_text, setup_complex_plane, ComplexPlotter
import math

class FactorialProp(Scene):
    def construct(self):
        chapter_title(self, "Concepts mathématiques", 1)
        cleanup = chapter_subtitle(self, "Concepts mathématiques", "La factorielle", 1, 1)

        # Definition
        fact_def = MathTex(r"n! = 1 \times 2 \times 3 \times \dots \times n", color=Colors.text)
        self.play(Write(fact_def), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Example
        example = MathTex(r"5! = 1 \times 2 \times 3 \times 4 \times 5 = 120", color=Colors.text)
        self.play(ReplacementTransform(fact_def, example), run_time=Durations.animations)
        self.wait(Durations.pauses)
        self.play(FadeOut(example), run_time=Durations.animations)

        # Growth comparison
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 150, 20],
            axis_config={"color": Colors.text},
        ).add_coordinates()
        
        labels = axes.get_axis_labels(x_label="n", y_label="y")
        
        # Plots
        graph_fact = axes.plot(lambda x: math.gamma(x + 1), x_range=[0, 5.5], color=BLUE) # Gamma for factorial interpolation
        graph_exp = axes.plot(lambda x: math.exp(x), x_range=[0, 5.5], color=GREEN)
        graph_poly = axes.plot(lambda x: x**3, x_range=[0, 5.5], color=RED)
        
        label_fact = MathTex("n!", color=BLUE).next_to(graph_fact, UP, buff=0)
        label_exp = MathTex("e^x", color=GREEN).next_to(graph_exp, RIGHT, buff=0)
        label_poly = MathTex("x^3", color=RED).next_to(graph_poly, RIGHT, buff=0)

        self.play(Create(axes), Write(labels), run_time=Durations.animations)
        
        self.play(Create(graph_poly), Write(label_poly), run_time=Durations.animations)
        self.wait(0.5)
        self.play(Create(graph_exp), Write(label_exp), run_time=Durations.animations)
        self.wait(0.5)
        self.play(Create(graph_fact), Write(label_fact), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        explanation = Text("La factorielle grandit extrêmement vite.", font_size=24, color=Colors.text).to_edge(DOWN)
        self.play(Write(explanation), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Cleanup
        self.play(FadeOut(axes), FadeOut(labels), FadeOut(graph_fact), FadeOut(graph_exp), FadeOut(graph_poly), 
                  FadeOut(label_fact), FadeOut(label_exp), FadeOut(label_poly), FadeOut(explanation), run_time=Durations.animations)
        cleanup()

class InfiniteSeries(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Concepts mathématiques", "Les séries infinies", 1, 2)
        
        # Definition
        series_def = MathTex(r"S = \sum_{n=0}^{\infty} a_n = a_0 + a_1 + a_2 + \dots", color=Colors.text)
        self.play(Write(series_def), run_time=Durations.animations)
        self.wait(Durations.pauses)
        self.play(FadeOut(series_def), run_time=Durations.animations)
        
        # Geometric Series Example 1/2 + 1/4 + ...
        # Visual: Segments on a line [0, 1]
        number_line = NumberLine(x_range=[0, 2, 1], length=10, include_numbers=True, color=Colors.text)
        self.play(Create(number_line), run_time=Durations.animations)
        
        value = 0
        pointer = Arrow(start=UP, end=DOWN, color=RED).next_to(number_line.n2p(0), UP)
        
        self.play(Create(pointer), run_time=Durations.animations)
        
        terms = [1, 0.5, 0.25, 0.125, 0.0625]
        curr_val = 0
        
        formula = MathTex(r"\sum_{n=0}^{\infty} \left(\frac{1}{2}\right)^n = 1 + \frac{1}{2} + \frac{1}{4} + \dots = 2", color=Colors.text).to_edge(UP)
        self.play(Write(formula), run_time=Durations.animations)

        for term in terms:
            curr_val += term
            new_pos = number_line.n2p(curr_val)
            # Draw segment
            segment = Line(number_line.n2p(curr_val - term), new_pos, color=BLUE, stroke_width=10)
            self.play(Create(segment), pointer.animate.next_to(new_pos, UP), run_time=0.5)
        
        self.wait(Durations.pauses)
        
        # Convergence explanation
        explanation = Text("La somme converge vers 2.", font_size=32, color=Colors.text).next_to(number_line, DOWN)
        self.play(Write(explanation), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(number_line), FadeOut(pointer), FadeOut(formula), FadeOut(explanation), run_time=Durations.animations) # Don't fade segments explicitly or group them
        cleanup()

class Integrals(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Concepts mathématiques", "Les intégrales", 1, 3)
        
        axes = Axes(x_range=[0, 5], y_range=[0, 10], axis_config={"color": Colors.text})
        labels = axes.get_axis_labels()
        
        func = lambda x: 0.5 * x**2
        graph = axes.plot(func, color=BLUE)
        
        self.play(Create(axes), Write(labels), Create(graph), run_time=Durations.animations)
        
        # Area
        area = axes.get_area(graph, x_range=[0, 4], color=BLUE, opacity=0.5)
        self.play(FadeIn(area), run_time=Durations.animations)
        
        integral_tex = MathTex(r"\int_{0}^{4} \frac{1}{2}x^2 \, dx", color=Colors.text).to_corner(UR)
        self.play(Write(integral_tex), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        definition = Text("L'aire sous la courbe.", font_size=32, color=Colors.text).next_to(integral_tex, DOWN)
        self.play(Write(definition), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(axes), FadeOut(labels), FadeOut(graph), FadeOut(area), FadeOut(integral_tex), FadeOut(definition), run_time=Durations.animations)
        cleanup()

class ComplexFunctions(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Concepts mathématiques", "Les fonctions complexes", 1, 4)
        
        plane = setup_complex_plane()
        self.play(Create(plane), run_time=Durations.animations)
        
        # Show f(z) = z^2 transformation
        func_tex = MathTex(r"f(z) = z^2", color=Colors.text).add_background_rectangle().to_corner(UL)
        self.play(Write(func_tex), run_time=Durations.animations)
        
        self.wait(Durations.pauses)
        
        ComplexPlotter.plot_lines(self, lambda z: z**2, plane)
        
        self.wait(Durations.pauses)
        self.play(FadeOut(plane), FadeOut(func_tex), run_time=Durations.animations)
        cleanup()

class AnalyticContinuation(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, "Concepts mathématiques", "Prolongement analytique", 1, 5)

        # Geometric series revisit
        formula = MathTex(r"\sum_{n=0}^{\infty} z^n = \frac{1}{1-z}", color=Colors.text).to_edge(UP)
        condition = MathTex(r"|z| < 1", color=RED).next_to(formula, DOWN)
        
        self.play(Write(formula), Write(condition), run_time=Durations.animations)
        
        plane = setup_complex_plane(x_range=[-3, 3], y_range=[-3, 3])
        self.play(Create(plane), run_time=Durations.animations)
        
        # Highlight unit circle (domain of convergence)
        unit_circle = Circle(radius=1, color=RED, fill_opacity=0.2).set_z_index(2)
        self.play(FadeIn(unit_circle), run_time=Durations.animations)
        
        explanation = Text("La somme ne converge que dans le disque.", font_size=24, color=Colors.text).to_edge(DOWN).add_background_rectangle()
        self.play(Write(explanation), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Analytic continuation
        extension_text = Text("Mais la fonction 1/(1-z) existe partout (sauf z=1).", font_size=24, color=Colors.text).to_edge(DOWN).add_background_rectangle()
        
        full_domain_rect = Rectangle(width=10, height=10, color=GREEN, fill_opacity=0.2)
        hole = Circle(radius=0.1, color=Colors.background, fill_opacity=1).move_to([1, 0, 0]) # Hole at z=1
        
        # Need to punch a hole? Easiest visual: just show green everywhere else
        # Or better: Transform the red circle into the full plane minus point
        
        self.play(ReplacementTransform(explanation, extension_text), run_time=Durations.animations)
        self.play(
            unit_circle.animate.scale(10).set_color(GREEN).set_opacity(0.1),
            ReplacementTransform(condition, MathTex(r"z \neq 1", color=GREEN).next_to(formula, DOWN)),
            run_time=2
        )
        
        # Mark z=1
        dot = Dot(point=[1, 0, 0], color=RED)
        label_pole = MathTex("z=1").next_to(dot, UP)
        self.play(Create(dot), Write(label_pole), run_time=Durations.animations)
        
        final_text = Text("C'est le prolongement analytique.", font_size=32, color=Colors.text).to_edge(DOWN).add_background_rectangle()
        self.play(ReplacementTransform(extension_text, final_text), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        self.play(FadeOut(plane), FadeOut(formula), FadeOut(unit_circle), FadeOut(final_text), FadeOut(dot), FadeOut(label_pole), run_time=Durations.animations)
        cleanup()
