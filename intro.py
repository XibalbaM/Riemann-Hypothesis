from manim import *
from common import *

class Intro(Scene):
    def construct(self):
        # 1. Title Slide
        title = Text("L'hypothèse de Riemann", font_size=72, gradient=(BLUE_E, PURPLE_E))
        subtitle = Text("D'une idée pas si compliquée à un problème du millénaire", font_size=32, color=BLACK)
        by = Text("par Maël Porret et Boris Rennard", font_size=24, color=GRAY)
        
        line = Line(start=LEFT * 4, end=RIGHT * 4, color=BLACK)
        
        # Group and arrange
        title_group = VGroup(title, subtitle, line, by).arrange(DOWN, buff=0.5)
        title_group.center()
        
        self.play(
            Write(title),
            GrowFromCenter(line),
            run_time=1
        )
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.play(Write(by), run_time=1)
        self.wait(1)
        
        # Transition to TOC
        self.play(
            FadeOut(subtitle), 
            FadeOut(by), 
            FadeOut(line),
            title.animate.scale(0.6).to_edge(UP),
            run_time=1
        )
        
        # 2. Table of Contents
        self.next_section("Table of Contents")
        
        toc_title = Text("Table des matières", font_size=40, color=BLACK).next_to(title, DOWN)
        self.play(Write(toc_title), run_time=1)
        
        # Data structure for TOC
        
        # Layout calculation
        # We'll put Ch 1 & 2 on the left, Ch 3 & 4 on the right? 
        # Or just a scrolling list? 
        # Let's try 2 columns for better density.
        
        # Layout calculation
        
        chapter_groups = []
        for i, (chap_name, subchaps) in enumerate(chapters):
            # Use same gradient as main title
            chap_text = Text(str(i + 1) + ". " + chap_name, font_size=24, gradient=(BLUE_E, PURPLE_E))
            sub_group = VGroup()
            for j, sub in enumerate(subchaps):
                sub_text = Text(str(i + 1) + "." + str(j + 1) + ". " + sub, font_size=18, color=BLACK)
                sub_group.add(sub_text)
            
            sub_group.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            full_chap = VGroup(chap_text, sub_group).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            chapter_groups.append(full_chap)
            
        chapters_group = VGroup(*chapter_groups).arrange_in_grid(rows=2, cols=2, buff=0.5, cell_alignment=UL).next_to(toc_title, DOWN, buff=1)
        
        # Animate
        self.play(
            Write(chapters_group),
            run_time=2
        )
        
        self.wait(2)
        
        # Cleanup
        self.play(
            FadeOut(title), 
            FadeOut(toc_title), 
            FadeOut(chapters_group),
            run_time=1
        )