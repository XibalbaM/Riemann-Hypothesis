from manim import *
from common import Colors, Durations

class Intro(Scene):
    def construct(self):
        # 1. Title Slide
        title = Text("L'hypothèse de Riemann", font_size=72, gradient=(BLUE_E, PURPLE_E))
        subtitle = Text("D'une idée qui a l'air évidente à un problème du millénaire", font_size=32, color=Colors.text)
        by = Text("par Maël Porret et Boris Rennard", font_size=24, color=GRAY)
        
        line = Line(start=LEFT * 4, end=RIGHT * 4, color=Colors.text)
        
        # Group and arrange
        title_group = VGroup(title, subtitle, line, by).arrange(DOWN, buff=0.5)
        title_group.center()
        
        self.play(
            Write(title),
            GrowFromCenter(line),
            run_time=Durations.animations
        )
        self.play(FadeIn(subtitle, shift=UP), run_time=Durations.animations)
        self.play(Write(by), run_time=Durations.animations)
        self.wait(Durations.pauses)
        
        # Transition to TOC
        self.play(
            FadeOut(subtitle), 
            FadeOut(by), 
            FadeOut(line),
            title.animate.scale(0.6).to_edge(UP),
            run_time=Durations.animations
        )
        
        # 2. Table of Contents
        self.next_section("Table of Contents")
        
        toc_title = Text("Table des matières", font_size=40, color=Colors.text).next_to(title, DOWN, buff=0.5)
        self.play(Write(toc_title), run_time=Durations.animations)
        
        # Data structure for TOC
        chapters = [
            ("1. Concepts mathématiques", [
                "1.1. La factorielle",
                "1.2. Les séries infinies",
                "1.3. Les intégrales",
                "1.4. Fonctions complexes",
                "1.5. Continuations analytiques"
            ]),
            ("2. La fonction zeta", [
                "2.1. Continuation analytique",
                "2.2. Différentes définitions",
                "2.3. Lien avec la factorielle",
                "2.4. Fun fact"
            ]),
            ("3. Les zéros de la fonction zeta", [
                "3.1. Zéros triviaux",
                "3.2. Zéros non-triviaux",
                "3.3. Avancées historiques",
                "3.4. L’hypothèse de Riemann",
                "3.5. Problèmes du millénaire"
            ]),
            ("4. Conséquences", [
                "4.1. Théorème des nombres premiers",
                "4.2. Autres conséquences"
            ]),
        ]
        
        # Layout calculation
        # We'll put Ch 1 & 2 on the left, Ch 3 & 4 on the right? 
        # Or just a scrolling list? 
        # Let's try 2 columns for better density.
        
        # Layout calculation
        
        chapter_groups = []
        for i, (chap_name, subchaps) in enumerate(chapters):
            # Use same gradient as main title
            chap_text = Text(chap_name, font_size=24, gradient=(BLUE_E, PURPLE_E))
            sub_group = VGroup()
            for sub in subchaps:
                sub_text = Text(sub, font_size=18, color=Colors.text)
                sub_group.add(sub_text)
            
            sub_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            full_chap = VGroup(chap_text, sub_group).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            chapter_groups.append(full_chap)
            
        c1, c2, c3, c4 = chapter_groups
        
        # Align row 1 (Chapters 1 and 3)
        c1.to_corner(UL, buff=1.0).shift(DOWN * 1.5)
        c3.to_corner(UR, buff=1.0).shift(DOWN * 1.5)
        # Ensure exact vertical alignment of tops
        c3.align_to(c1, UP)
        
        # Align row 2 (Chapters 2 and 4)
        # Determine the Y position based on the lowest point of row 1 to ensure no overlap
        # buffer of 0.8
        y_pos = min(c1.get_bottom()[1], c3.get_bottom()[1]) - 0.8
        
        # Align Left edges of c2 to c1, and c4 to c3
        c2.move_to([c1.get_left()[0], y_pos, 0], aligned_edge=UL)
        c4.move_to([c3.get_left()[0], y_pos, 0], aligned_edge=UL)
        
        # Animate
        self.play(
            LaggedStart(
                Write(c1), Write(c3),
                lag_ratio=0.5,
                run_time=2
            )
        )
        self.play(
            LaggedStart(
                Write(c2), Write(c4),
                lag_ratio=0.5,
                run_time=2
            )
        )
        
        self.wait(Durations.pauses * 2)
        
        # Cleanup
        self.play(
            FadeOut(title), 
            FadeOut(toc_title), 
            FadeOut(c1), FadeOut(c2), FadeOut(c3), FadeOut(c4),
            run_time=Durations.animations
        )