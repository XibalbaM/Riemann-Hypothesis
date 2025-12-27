from manim import *
from manim_slides import Slide
from types import SimpleNamespace
import numpy as np

Colors = SimpleNamespace(
    text=BLACK,
    background=WHITE,
    true=GREEN,
    false=RED
)

Durations = SimpleNamespace(
    animations=1,
    pauses=1
)

def ColorFromTruthValue(value: str):
    if value == "V":
        return Colors.true
    elif value == "F":
        return Colors.false
    else:
        return Colors.text
    
def chapter_title(scene: Slide, title_text: str, number: int):
    title = Text(title_text, font_size=48, color=Colors.text)
    group = VGroup(Text(f"Chapitre {number}", font_size=48, color=Colors.text).shift(UP * 2), title)
    scene.play(Write(group), run_time=Durations.animations)
    scene.wait(Durations.pauses)
    scene.play(FadeOut(group, shift=UP * 3), run_time=Durations.animations)

def chapter_subtitle(scene: Slide, title_text: str, subtitle_text: str, chapter_number: int, subchapter_number: int):
    title = Text(title_text, font_size=42, color=Colors.text).shift(UP)
    subtitle = Text(subtitle_text, font_size=32, color=Colors.text).next_to(title, DOWN)
    partie_text = Text(f"Partie {chapter_number}.{subchapter_number}", font_size=36, color=Colors.text).shift(UP * 2)
    group = VGroup(partie_text, title, subtitle)
    scene.play(Write(group), run_time=Durations.animations)
    scene.wait(Durations.pauses)
    top_title = Text(f"{chapter_number}.{subchapter_number} : {subtitle_text}", font_size=24, color=Colors.text).to_edge(UP)
    scene.play(Transform(subtitle, top_title), FadeOut(title), FadeOut(partie_text), run_time=Durations.animations)
    return lambda: scene.play(FadeOut(subtitle, shift=UP * 3), run_time=Durations.animations)

def wrap_text(text, max_chars=40):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line) + len(word) + 1 <= max_chars:
            line += (" " if line else "") + word
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return "\n".join(lines)

def get_complex_plot(func, x_range=[-5, 5], y_range=[-3, 3], mode="lines"):
    """
    Returns a VGroup containing the plot of the complex function `func`.
    mode can be:
    - "lines": Transform grid lines
    - "domain_coloring": (To be implemented or approximated with surface)
    """
    # For now, let's implement a basic line transformation or creating a complex plane
    # This is a placeholder for the more advanced switching logic requested
    
    if mode == "lines":
        plane = ComplexPlane(x_range=x_range, y_range=y_range, background_line_style={"stroke_opacity": 0.5})
        plane.add_coordinates()
        return plane.plot(lambda z: func(z)) # This might not be the standard manim way for complex mapping, let's check docs logic
        # Actually manim has ComplexFunctionGraph? Or we apply_complex_function to a grid?
        
    # Better approach for "switching":
    # We return a function that modifies a scene or returns a Mobject
    
    pass

class ComplexPlotter:
    @staticmethod
    def plot_lines(scene, func, plane):
        # Apply function to the plane
        scene.play(plane.animate.apply_complex_function(func), run_time=Durations.animations)

    @staticmethod
    def get_domain_coloring(func, x_range, y_range):
        # Placeholder for domain coloring: commonly done with ImageMobject and numpy
        pass

def setup_complex_plane(x_range=[-6, 6], y_range=[-4, 4]):
    plane = ComplexPlane(x_range=x_range + [1], y_range=y_range + [1])
    plane.add_coordinates()
    return plane