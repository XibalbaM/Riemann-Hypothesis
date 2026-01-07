from manim.animation.fading import FadeIn
from manim import *
from common import *
import numpy as np

class Part1_1_Integrals(Scene):
    def construct(self):
        # Show chapter title
        title_mobject = chapter_title(self, 1)        
        # Setup subtitle and header
        cleanup = chapter_subtitle(self, 1, 1, title_mobject=title_mobject)
        
        # 1. Visualize area under curve
        axes = Axes(
            x_range=[0, 5],
            y_range=[0, 5],
            axis_config={"color": BLACK}
        ).scale(0.8).shift(DOWN*0.5)
        
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        labels.set_color(BLACK)
        a_label = MathTex("a", color=BLACK).next_to(axes.c2p(1, 0), DOWN)
        b_label = MathTex("b", color=BLACK).next_to(axes.c2p(4, 0), DOWN)
        
        # Smooth function: x*sin(x) + 2 scaled a bit
        def func(x):
            return 0.5 * x * np.sin(x) + 2
        
        graph = axes.plot(func, color=BLUE_E)
        area = axes.get_area(graph, x_range=[1, 4], color=BLUE_E, opacity=0.3)
        
        integral_tex = MathTex(r"\int_a^b f(x) dx\approx 6.78", color=BLACK).to_edge(RIGHT, buff=1).shift(UP*1)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2)
        self.play(FadeIn(area), Write(integral_tex), Write(a_label), Write(b_label))
        self.wait(2)
        self.play(FadeOut(axes), FadeOut(graph), FadeOut(labels), FadeOut(area), FadeOut(integral_tex), FadeOut(a_label), FadeOut(b_label))
        
        # 2. Fundamental Theorem of Calculus (Intuition)
        
        ftc_text = Text("Théorème Fondamental de l'Analyse", font_size=24, color=BLUE_E).to_edge(UP, buff=1.5)
        ftc_formula = MathTex(r"\frac{d}{dx} \int_a^x f(t) dt = f(x)", color=BLACK).next_to(ftc_text, DOWN)
        
        self.play(Write(ftc_text))
        self.play(Write(ftc_formula))
        self.wait(3)
        
        self.play(FadeOut(ftc_text), FadeOut(ftc_formula), cleanup)

class Part1_2_ComplexAnalysis(ThreeDScene):
    def construct(self):
        cleanup = chapter_subtitle(self, 1, 2)
        
        # 1. How to plot complex functions
        plane = ComplexPlane(
            axis_config={"color": BLACK},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        )
        base_plane = plane.copy()
        # Another type of complex plane : a grid of particles
        points = VGroup()
        step = 0.25
        def get_color(x, y):
            return interpolate_color(BLUE_E, GREEN_E, (x + 5) / 10) # example
        for x in np.arange(-config.frame_width/2, config.frame_width/2 + step, step):
            for y in np.arange(-config.frame_height/2, config.frame_height/2 + step, step):
                points.add(Dot(plane.c2p(x, y), color=get_color(x, y), radius=0.04))
        
        # Keep a copy of initial state to be able to reset
        points_initial = points.copy()

        self.play(Create(plane))
        self.wait(1)

        # 1.1. Solution 1 : Plotting the transformation of the complex plane by a function
        
        # z -> z^2
        self.play(plane.animate.apply_complex_function(lambda z: z**2), run_time=3)
        self.wait(1)

        # z -> 1/z
        # Show the grid of particles
        self.play(Transform(plane, base_plane), FadeIn(points))
        self.wait(1)

        # We transform centers only to avoid scaling the dots
        target_points_inv = points.copy()
        for dot in target_points_inv:
            z = plane.p2n(dot.get_center())
            if abs(z) < 0.1: z = 0.1 # Avoid infinity
            target_pos = plane.n2p(1/z)
            dot.move_to(target_pos)
            
        self.play(
            plane.animate.apply_complex_function(lambda z: 1/z),
            Transform(points, target_points_inv),
            run_time=3
        )
        self.wait(1)

        # z -> exp(z)
        # Show the grid of particles
        self.play(Transform(plane, base_plane), Transform(points, points_initial))
        self.wait(1)

        # We transform centers only to avoid scaling the dots
        target_points_exp = points.copy()
        for dot in target_points_exp:
            z = plane.p2n(dot.get_center())
            target_pos = plane.n2p(np.exp(z))
            dot.move_to(target_pos)
            
        self.play(
            plane.animate.apply_complex_function(np.exp),
            Transform(points, target_points_exp),
            run_time=3
        )
        self.wait(1)
        
        # z -> sin(z)
        # Reset plane and points
        self.play(Transform(plane, base_plane), Transform(points, points_initial))
        self.wait(1)

        target_points_sin = points.copy()
        for dot in target_points_sin:
            z = plane.p2n(dot.get_center())
            target_pos = plane.n2p(np.sin(z))
            dot.move_to(target_pos)
            
        self.play(
            plane.animate.apply_complex_function(np.sin),
            Transform(points, target_points_sin),
            run_time=3
        )
        self.wait(1)

        self.play(FadeOut(plane), FadeOut(points))
        
        # 1.2. Solution 2 : Plotting only one component of the output via color (real part, imaginary part, absolute value, argument), possibly using multiple plots

        # f(z)=z^3-z^2+z-1
        def f(z):
            return z**3 - z**2 + z - 1

        axes3d = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
            z_length=4,
            axis_config={"color": BLACK}
        ).shift(LEFT * 2)

        # Helper for surfaces
        def get_surface(func):
            return Surface(
                lambda u, v: axes3d.c2p(u, v, func(complex(u, v))),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(20, 20),
                fill_opacity=0.7,
                checkerboard_colors=[BLUE_D, BLUE_E]
            )

        # 1. Re(f(z)) with 3d
        label_re = MathTex(r"\text{Re}(f(z))", color=BLACK).next_to(axes3d, RIGHT, buff=1).shift(UP*2)
        surface_re = get_surface(lambda z: f(z).real)
        
        self.play(Create(axes3d), Write(label_re))
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(Create(surface_re))
        self.wait(2)

        # Go back to 2D
        self.play(FadeOut(surface_re), FadeOut(axes3d), FadeOut(label_re))
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2)

        # 2. Using color
        heatmap = always_redraw(lambda: HeatmapMobject(
            function=f,
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=4,
            y_length=4
        ))
        
        self.play(FadeIn(heatmap))
        self.wait(2)
        self.play(FadeOut(heatmap), cleanup)

class Part1_3_InfiniteSeries(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 1, 3)
        
        # 1. Geometric Series Example
        series_tex = MathTex(r"\sum_{n=1}^\infty \frac{1}{2^n} = 1", color=BLACK).shift(UP*2)
        self.play(Write(series_tex))
        
        # Number Line Visualization
        line = NumberLine(
            x_range=[0, 1.1, 0.5],
            length=10,
            color=BLACK,
            include_numbers=True,
            label_direction=DOWN,
            font_size=24
        ).shift(DOWN * 0.5)
        
        segments = VGroup()
        labels = VGroup()
        current_sum = 0
        colors = [BLUE_E, TEAL, GREEN_E, YELLOW, ORANGE, RED_E]
        
        for i in range(1, 7):
            term = 1 / (2**i)
            start_p = line.n2p(current_sum)
            end_p = line.n2p(current_sum + term)
            
            segment = Line(start_p, end_p, color=colors[i-1], stroke_width=10)
            # Add a small vertical tick at the end
            tick = Line(UP*0.1, DOWN*0.1, color=BLACK).move_to(end_p)
            segment.add(tick)
            
            if i <= 3:
                label = MathTex(rf"\frac{{1}}{{{2**i}}}", color=BLACK, font_size=24).next_to(segment, UP, buff=0.2)
                labels.add(label)
                
            segments.add(segment)
            current_sum += term

        self.play(Create(line))
        self.play(
            LaggedStart(
                *[Create(seg) for seg in segments],
                lag_ratio=0.5,
                 run_time=4
            ),
            LaggedStart(
                *[Write(lab) for lab in labels],
                lag_ratio=0.5,
                run_time=3
            )
        )
        self.wait(1)
        
        self.play(FadeOut(segments), FadeOut(labels), FadeOut(line), FadeOut(series_tex))

        # 2. General Formula
        formula = MathTex(r"\sum_{n=0}^N r^n = \frac{1-r^{N+1}}{1-r}", color=BLACK)
        formula2 = MathTex(r"\sum_{n=0}^\infty r^n = \frac{1}{1-r} \text{ pour } |r| < 1", color=BLACK)
        self.play(Write(formula))
        self.wait(3)
        
        self.play(Transform(formula, formula2))
        self.wait(3)
        
        self.play(FadeOut(formula), cleanup)

class Part1_4_AnalyticContinuation(Scene):
    def construct(self):
        cleanup = chapter_subtitle(self, 1, 4)
        
        # An example
        func_f = MathTex(r"f(z) = \sum_{n=0}^\infty z^n", color=BLACK).shift(UP*2 + LEFT*3)
        domain_f = Text("Défini pour |z| < 1", font_size=20, color=BLACK).next_to(func_f, DOWN)
        
        func_g = MathTex(r"g(z) = \frac{1}{1-z}", color=BLACK).shift(UP*2 + RIGHT*3)
        domain_g = Text("Défini partout sauf z = 1", font_size=20, color=BLACK).next_to(func_g, DOWN)
        
        self.play(Create(func_f), Write(domain_f))
        self.wait(1)
        self.play(Create(func_g), Write(domain_g))
        self.wait(1)

        self.play(FadeOut(func_f), FadeOut(domain_f), FadeOut(func_g), FadeOut(domain_g))

        # What is a good continuation ?
        axes = Axes(x_range=[-10, 10], y_range=[-10, 10], axis_config={"color": BLACK})
        labels = axes.get_axis_labels("x", "y")
        
        line = axes.plot(lambda x: x, color=BLUE_E, x_range=[-2.5, 2.5])
        self.play(Create(axes), Create(line), Write(labels))
        self.wait(1)

        proper_continuation = axes.plot(lambda x: x, color=GREEN_E, x_range=[2.5, 10])
        improper_continuation = axes.plot(lambda x: np.exp(np.log(2.5)/2.5*x), color=ORANGE, x_range=[2.5, 10])
        improper_continuation2 = axes.plot(lambda x: 2.5*np.sin(np.pi * x / 5), color=RED_E, x_range=[2.5, 10])
        self.play(Create(proper_continuation), Create(improper_continuation), Create(improper_continuation2))
        self.wait(1)

        self.play(FadeOut(line), FadeOut(axes), FadeOut(labels), FadeOut(proper_continuation), FadeOut(improper_continuation), FadeOut(improper_continuation2))

        # Taylor series of e^x
        
        # New axes for Taylor Series
        taylor_axes = Axes(x_range=[-4, 4], y_range=[-2, 10], axis_config={"color": BLACK}).scale(0.8)
        taylor_labels = taylor_axes.get_axis_labels("x", "f(x)")
        
        func_exp = taylor_axes.plot(np.exp, color=BLUE_E)
        label_exp = MathTex("e^x", color=BLUE_E).next_to(func_exp, UP, buff=0.5)
        
        self.play(Create(taylor_axes), Create(func_exp), Write(taylor_labels), Write(label_exp))
        self.wait(1)
        
        # Taylor polynomials of e^x at 0: 1 + x + x^2/2 + ...
        # P_n(x) = sum_{k=0}^n x^k / k!
        
        import math
        
        prev_poly = None
        poly_label = None
        
        for n in range(10):
            # Define the n-th Taylor polynomial
            def taylor_poly(x, degree=n):
                return sum([(x**k)/math.factorial(k) for k in range(degree + 1)])
            
            poly = taylor_axes.plot(lambda x: taylor_poly(x, n), color=RED_E, x_range=[-4, 4])
            
            # Construct the formula string
            # We'll just show the last term added or simple summation
            if n == 0:
                tex = "1"
            elif n == 1:
                tex = "1 + x"
            elif n == 2:
                tex = "1 + x + \\frac{x^2}{2}"
            elif n == 3:
                tex = "1 + x + \\frac{x^2}{2} + \\frac{x^3}{6}"
            else:
                tex = f"P_{{{n}}}(x) = \\sum_{{k=0}}^{{{n}}} \\frac{{x^k}}{{k!}}"
                
            new_label = MathTex(tex, color=RED_E, font_size=36).to_edge(UP, buff=1.5).shift(RIGHT*3)
            
            if prev_poly is None:
                self.play(Create(poly), Write(new_label))
                prev_poly = poly
                poly_label = new_label
            else:
                self.play(Transform(prev_poly, poly), Transform(poly_label, new_label), run_time=1)
                
            self.wait(1/(n+1))
            
        self.wait(2)
        self.play(FadeOut(taylor_axes), FadeOut(func_exp), FadeOut(taylor_labels), FadeOut(label_exp), FadeOut(prev_poly), FadeOut(poly_label))
        
        # Interpolation
        interp_axes = Axes(x_range=[-1, 5], y_range=[-5, 5], axis_config={"color": BLACK}).scale(0.8)
        
        # Define 5 points
        points_x = [0, 1, 2, 3, 4]
        points_y = [0, 2, -1, 3, 0] # Arbitrary values
        
        dots = VGroup()
        for x, y in zip(points_x, points_y):
            dots.add(Dot(interp_axes.c2p(x, y), color=BLACK, radius=0.08))
            
        self.play(Create(interp_axes), FadeIn(dots))
        self.wait(1)
        
        # Calculate interpolating polynomial using numpy
        coeffs = np.polyfit(points_x, points_y, len(points_x)-1)
        poly_func = np.poly1d(coeffs)
        
        interp_curve = interp_axes.plot(poly_func, color=BLUE_E, x_range=[-1, 5])
        poly_tex = f"P(x) = {coeffs[0].round(2)}x^4 + {coeffs[1].round(2)}x^3 + {coeffs[2].round(2)}x^2 + {coeffs[3].round(2)}x + {coeffs[4].round(2)}"
        interp_label = MathTex(poly_tex, color=BLUE_E).next_to(interp_curve, UP, buff=0.5)
        
        self.play(Create(interp_curve), Write(interp_label))
        self.wait(3)
        # TODO : Add giggling

        # Add one more point
        points_x.append(5)
        points_y.append(2)

        dots.add(Dot(interp_axes.c2p(5, 2), color=BLACK, radius=0.08))
        self.play(FadeIn(dots[-1]))

        coeffs = np.polyfit(points_x, points_y, len(points_x)-1)
        poly_func = np.poly1d(coeffs)
        
        interp_curve2 = interp_axes.plot(poly_func, color=BLUE_E, x_range=[-1, 5])
        poly_tex2 = f"P(x) = {coeffs[0].round(2)}x^5 + {coeffs[1].round(2)}x^4 + {coeffs[2].round(2)}x^3 + {coeffs[3].round(2)}x^2 + {coeffs[4].round(2)}x + {coeffs[5].round(2)}"
        interp_label2 = MathTex(poly_tex2, color=BLUE_E).next_to(interp_curve2, UP, buff=0.5)
        self.play(Transform(interp_curve, interp_curve2), Transform(interp_label, interp_label2))
        self.wait(3)
        
        self.play(FadeOut(interp_axes), FadeOut(dots), FadeOut(interp_curve))
        self.play(cleanup)

class Part1_5_GammaFunction(Scene):
    def construct(self):
        import math
        cleanup = chapter_subtitle(self, 1, 5)

        # 1. Connecting factorial dots
        
        # Axes
        axes = Axes(
            x_range=[-0.5, 4.5, 1],
            y_range=[-1, 7, 1],
            axis_config={"color": BLACK}
        ).scale(0.8)
        
        labels = axes.get_axis_labels("x", "y")
        
        self.play(Create(axes), Write(labels))
        
        # Points (n, n!)
        points_data = [(0, 1), (1, 1), (2, 2), (3, 6)]
        dots = VGroup()
        for x, y in points_data:
            dots.add(Dot(axes.c2p(x, y), color=BLUE_E, radius=0.08))
            
        self.play(FadeIn(dots))
        self.wait(0.5)
        
        question = Text("Comment relier ces points ?", font_size=24, color=BLACK).to_edge(UP, buff=1.5)
        self.play(Write(question))
        self.wait(1)
        
        # Gamma curve: f(x) = Gamma(x+1)
        # Note: math.gamma takes real numbers.
        gamma_curve = axes.plot(lambda x: math.gamma(x+1), color=RED_E, x_range=[-0.45, 3.5])
        
        label_gamma = MathTex(r"\Gamma(x+1) = x!", color=RED_E).next_to(gamma_curve, RIGHT, buff=0.1).shift(UP*0.5)
        
        self.play(Create(gamma_curve), Write(label_gamma))
        self.wait(2)
        
        self.play(FadeOut(dots), FadeOut(gamma_curve), FadeOut(axes), FadeOut(labels), FadeOut(question), FadeOut(label_gamma))

        # 2. The gamma function expression
        title_def = Text("La Fonction Gamma", font_size=36, color=BLUE_E).to_edge(UP, buff=1.5)
        def_tex = MathTex(r"\Gamma(z) = \int_0^\infty t^{z-1} e^{-t} dt", color=BLACK).scale(1.2).shift(UP*0.5)
        
        prop_tex = MathTex(r"\Gamma(n) = (n-1)!", color=BLACK).next_to(def_tex, DOWN, buff=1)
        
        self.play(Write(title_def))
        self.play(Write(def_tex))
        self.wait(1)
        self.play(Write(prop_tex))
        self.wait(2)
        
        self.play(FadeOut(def_tex), FadeOut(prop_tex))

        # 3. Few properties and values
        props = VGroup(
            MathTex(r"\Gamma(z+1) = z\Gamma(z)", color=BLACK),
            MathTex(r"\Gamma(1/2) = \sqrt{\pi}", color=BLACK),
            MathTex(r"\Gamma(-1/2) = -2\sqrt{\pi}", color=BLACK)
        ).arrange(DOWN, buff=0.5).shift(UP*0.5)
        
        self.play(Write(props))
        self.wait(3)
        self.play(FadeOut(props))

        # 4. A way to take irrational derivatives
        # Introduction
        deriv_title = Text("Dérivées fractionnaires ?", font_size=36, color=BLUE_E).to_edge(UP, buff=1.5)
        
        self.play(Transform(title_def, deriv_title))
        
        # Standard derivative power rule
        rule_int = MathTex(r"\frac{d^n}{dx^n} x^k = \frac{k!}{(k-n)!} x^{k-n}", color=BLACK)
        self.play(Write(rule_int))
        self.wait(2)
        
        # Generalized
        rule_frac = MathTex(r"\frac{d^\alpha}{dx^\alpha} x^k = \frac{\Gamma(k+1)}{\Gamma(k-\alpha+1)} x^{k-\alpha}", color=BLACK)
        
        self.play(ReplacementTransform(rule_int, rule_frac))
        self.wait(1)
        
        self.play(rule_frac.animate.to_edge(UP, buff=2.5))
        
        # Example
        example = MathTex(r"\frac{d^{\pi}}{dx^{\pi}} x = \frac{\Gamma(2)}{\Gamma(1-\pi)} x^{1-\pi} = \frac{2}{\Gamma(1-\pi)} x^{1-\pi}", color=BLACK).scale(1)
        
        self.play(Write(example))
        self.wait(3)
        
        self.play(FadeOut(example), FadeOut(rule_frac), FadeOut(title_def), cleanup)