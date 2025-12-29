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

def get_color_scale(colors, label_text, vrange=[0, 1]):
    scale = VGroup()
    for i, color in enumerate(colors):
        rect = Square(side_length=0.2, fill_color=color, fill_opacity=1, stroke_width=0)
        rect.shift(DOWN * i * 0.2)
        scale.add(rect)
    scale.to_edge(RIGHT, buff=1)
    label = Text(label_text, font_size=20, color=BLACK).next_to(scale, UP)
    min_l = Text(str(vrange[0]), font_size=16, color=BLACK).next_to(scale, RIGHT).align_to(scale, UP)
    max_l = Text(str(vrange[1]), font_size=16, color=BLACK).next_to(scale, RIGHT).align_to(scale, DOWN)
    return VGroup(scale, label, min_l, max_l)

def get_continuous_image(func, x_range=[-6, 6], y_range=[-4, 4], res_x=256, res_y=256, mode="mag", v_max=10):
    x = np.linspace(x_range[0], x_range[1], res_x)
    y = np.linspace(y_range[1], y_range[0], res_y)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Vectorize func manually to handle potential issues with mpmath complex types
    W = np.zeros(Z.shape, dtype=complex)
    for i in range(res_y):
        for j in range(res_x):
            try:
                W[i, j] = complex(func(Z[i, j]))
            except:
                W[i, j] = 0
    
    if mode == "mag":
        Mag = np.abs(W)
        T = np.clip(Mag / v_max, 0, 1)
        c1 = np.array(color_to_rgb(BLUE_E))
        c2 = np.array(color_to_rgb(RED))
        RGB = c1[None, None, :] + T[:, :, None] * (c2 - c1)[None, None, :]
    else: # Phase / Argument
        Arg = np.angle(W)
        T = (Arg + np.pi) / (2 * np.pi)
        colors = [RED, YELLOW, GREEN, BLUE, PURPLE, RED]
        rgb_colors = [np.array(color_to_rgb(c)) for c in colors]
        RGB = np.zeros((res_y, res_x, 3))
        for k in range(5):
            mask = (T >= k/5) & (T <= (k+1)/5)
            if not np.any(mask): continue
            t_sub = (T[mask] - k/5) * 5
            RGB[mask] = rgb_colors[k][None, :] + t_sub[:, None] * (rgb_colors[k+1] - rgb_colors[k])[None, :]
    
    img = ImageMobject((RGB * 255).astype(np.uint8))
    img.height = 8
    img.width = 12
    return img