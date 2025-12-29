from manim.animation.growing import SpinInFromNothing
from manim import *
import numpy as np

chapters = [
    ("Concepts mathématiques", [
        "Intégrales",
        "Analyse dans le plan complexe",
        "Séries infinies",
        "Continuations analytiques"
    ]),
    ("La fonction zêta", [
        "Fonction zêta",
        "Premières valeurs calculées",
        "Continuation analytique",
        "Différentes définitions",
    ]),
    ("Les zéros de la fonction zêta", [
        "Zéros triviaux",
        "Zéros non-triviaux",
        "Avancées historiques",
        "L’hypothèse de Riemann",
        "Problèmes du millénaire"
    ]),
    ("Conséquences", [
        "Théorème des nombres premiers",
        "Le théorème de Riemann sur la fonction pi",
        "Autres conséquences"
    ]),
]

def ColorFromTruthValue(value: str):
    if value == "V":
        return GREEN
    elif value == "F":
        return RED
    else:
        return BLACK
    
def chapter_title(scene: Scene, number: int):
    title = Text(chapters[number - 1][0], font_size=48, color=BLACK)
    chapter = Text(f"Chapitre {number}", font_size=48, color=BLACK).shift(UP * 2)
    line = Line(LEFT, RIGHT, color=BLACK).scale(4).next_to(title, DOWN, buff=0.2)
    scene.play(Write(title), Write(chapter), GrowFromCenter(line), run_time=1)
    scene.wait(1)
    scene.play(FadeOut(chapter),FadeOut(line), run_time=1)
    return title

def chapter_subtitle(scene: Scene, chapter_number: int, subchapter_number: int, title_mobject: Mobject = None):
    title = Text(chapters[chapter_number - 1][0], font_size=42, color=BLACK, weight=BOLD).shift(UP)
    subtitle = Text(chapters[chapter_number - 1][1][subchapter_number - 1], font_size=32, color=BLACK).next_to(title, DOWN)
    partie_text = Text(f"Partie {chapter_number}.{subchapter_number}", font_size=36, color=BLACK).shift(UP * 2)
    
    if title_mobject:
        scene.play(ReplacementTransform(title_mobject, title), Write(subtitle), Write(partie_text), run_time=1)
    else:
        scene.play(Write(title), Write(subtitle), Write(partie_text), run_time=1)
    scene.wait(1)
    
    top_title = Text(f"{chapter_number}.{subchapter_number} : {chapters[chapter_number - 1][1][subchapter_number - 1]}", font_size=24, color=BLACK, weight=BOLD).to_edge(UP, buff=0.25)
    
    scene.play(
        Transform(subtitle, top_title),
        FadeOut(title),
        FadeOut(partie_text),
        run_time=1
    )
    
    return Unwrite(subtitle, run_time=1)

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