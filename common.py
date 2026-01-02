from manim.animation.growing import SpinInFromNothing
from manim import *
import numpy as np
import matplotlib.pyplot as plt

chapters = [
    ("Concepts mathématiques", [
        "Intégrales",
        "Analyse dans le plan complexe",
        "Séries infinies",
        "Continuations analytiques",
        # Fonction gamma
    ]),
    ("La fonction zêta", [
        "Premières valeurs calculées",
        "Études de la série dans le plan complexe",
        "Différentes définitions",
    ]),
    ("Les zéros de la fonction zêta", [
        "Zéros triviaux",
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
    top_title.set_z_index(2)
    
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

def HeatmapMobject(function, x_range, y_range, x_length, y_length, mode="hue", **kwargs):
    x_min, x_max = x_range
    y_min, y_max = y_range
    
    resolution = 25
    
    # Resolution
    width = int(x_length * resolution)
    height = int(y_length * resolution)

    # Create grid
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    # Evaluate function
    vals = np.vectorize(function)(Z)
    if mode == "hue":
        
        # 1. Hue from Argument
        # arg(z) in (-pi, pi) -> map to (0, 1)
        # adding pi makes it (0, 2pi), divide by 2pi
        h = (np.angle(vals) + np.pi) / (2 * np.pi)
        
        # 2. Brightness (Value) from Log Magnitude
        mags = np.abs(vals)
        # Handle zeros: if mag is 0, log is -inf. We want black.
        # We can add a small epsilon or clip.
        # But usually 0 magnitude -> V=0 (Black).
        # Since we need to normalize log scale to [0, 1], we need a range.
        # Let's compute log magnitudes, guarding against 0.
        
        # Replace 0 with a very small number for log calculation
        mags_safe = np.where(mags == 0, 1e-9, mags)
        log_mags = np.log(mags_safe)
        
        # Normalize log_mags to [0, 1] relative to the view
        min_log = np.min(log_mags)
        max_log = np.max(log_mags)
        
        if max_log == min_log:
            v = np.ones_like(log_mags) # Flat brightness if constant magnitude
        else:
            v = (log_mags - min_log) / (max_log - min_log)
            
        # Saturation is usually 1 for full color
        s = np.ones_like(h) * 0.8 # slightly less than 1 for smoother look? Or 1. 0.8 is safer for aesthetics.
        # previous user code used s=0.8, v=0.9
        
        # Convert HSV to RGB manually vectorized
        # h is [0, 1], s is [0, 1], v is [0, 1]
        
        i = (h * 6.0).astype(int)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - f * s)
        t = v * (1.0 - (1.0 - f) * s)
        
        i = i % 6
        
        r = np.zeros_like(h)
        g = np.zeros_like(h)
        b = np.zeros_like(h)
        
        idx = (i == 0)
        r[idx], g[idx], b[idx] = v[idx], t[idx], p[idx]
        
        idx = (i == 1)
        r[idx], g[idx], b[idx] = q[idx], v[idx], p[idx]
        
        idx = (i == 2)
        r[idx], g[idx], b[idx] = p[idx], v[idx], t[idx]
        
        idx = (i == 3)
        r[idx], g[idx], b[idx] = p[idx], q[idx], v[idx]
        
        idx = (i == 4)
        r[idx], g[idx], b[idx] = t[idx], p[idx], v[idx]
        
        idx = (i == 5)
        r[idx], g[idx], b[idx] = v[idx], p[idx], q[idx]
        
        # Stack to structure (height, width, 3)
        rgb = np.dstack((r, g, b))
    
        # Add alpha
        alpha = np.ones((height, width, 1))
        rgba = np.concatenate([rgb, alpha], axis=2)
    elif mode == "magn" or mode == "log":
        # Take only magintude into account, red to blue
        mags = np.abs(vals)
        if mode == "log":
            mags = np.log(mags)
        
        # Normalize mags to [0, 1] relative to the view
        min_mag = np.min(mags)
        max_mag = np.max(mags)
        
        if max_mag == min_mag:
            v = np.ones_like(mags) # Flat brightness if constant magnitude
        else:
            v = (mags - min_mag) / (max_mag - min_mag)
            
        # Convert to RGB
        rgba = plt.cm.coolwarm(v)

    # Convert to unit8
    pixel_array = (rgba * 255).astype(np.uint8)
    
    img = ImageMobject(pixel_array, **kwargs)
    img.width = x_length
    img.height = y_length
    
    # Store attributes (might be useful for some scale, though standard color scales don't apply well to domain coloring)
    img.min_val = np.min(mags) # Raw magnitude min
    img.max_val = np.max(mags)
    # img.colors = ... # No specific color list anymore
    
    return img