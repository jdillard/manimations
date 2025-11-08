from manim import *

class ComplexityConsciousness(Scene):
    def construct(self):
        # Set dark background
        self.camera.background_color = "#001a33"  # Dark blue

        # Create the title
        title = Text(
            "Law of Complexity-Consciousness",
            font_size=48,
            color=WHITE
        ).to_edge(UP, buff=0.5)

        # Create axes with custom range and labels
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=10,
            y_length=6,
            axis_config={
                "color": BLUE_C,
                "stroke_width": 2,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2,
            },
            tips=True,
        ).shift(DOWN * 0.5)

        # Create axis labels
        x_label = Text(
            "Material Complexity",
            font_size=32,
            color=BLUE_C
        ).next_to(axes.x_axis, DOWN, buff=0.3).shift(RIGHT * 2)

        y_label = Text(
            "Consciousness",
            font_size=32,
            color=BLUE_C
        ).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI / 2).shift(UP * 1)

        # Create subtle grid lines
        grid = NumberPlane(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=10,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 0.5,
                "stroke_opacity": 0.15,
            },
            faded_line_ratio=4,
        ).shift(DOWN * 0.5)

        # Animate the scene construction
        self.play(FadeIn(title), run_time=1)
        self.wait(0.5)

        # Show grid first (background)
        self.play(Create(grid), run_time=1.5)

        # Then show axes
        self.play(
            Create(axes),
            run_time=2,
            rate_func=smooth
        )

        # Finally show labels
        self.play(
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )

        self.wait(0.5)

        # ===== COMMIT 2: THE CORRELATION CURVE =====

        # Define the complexity-consciousness correlation function
        # Using a logarithmic curve that starts near origin and curves upward
        def complexity_curve(x):
            # Logarithmic growth: y = a * log(x + 1) + b * x^0.7
            # This creates a curve that accelerates upward
            return 2.5 * np.log(x + 1) + 0.4 * (x ** 0.7)

        # Create the main curve
        curve = axes.plot(
            complexity_curve,
            x_range=[0, 9.5],
            color=BLUE,
            stroke_width=4,
        )

        # Apply gradient coloring: blue → purple → orange → white
        curve.set_color_by_gradient(BLUE, PURPLE, ORANGE, WHITE)

        # Create glow effect (wider, semi-transparent copy behind the curve)
        glow = axes.plot(
            complexity_curve,
            x_range=[0, 9.5],
            stroke_width=12,
            stroke_opacity=0.4,
        )
        glow.set_color_by_gradient(BLUE, PURPLE, ORANGE, WHITE)

        # Create a second, softer glow layer
        glow_soft = axes.plot(
            complexity_curve,
            x_range=[0, 9.5],
            stroke_width=20,
            stroke_opacity=0.2,
        )
        glow_soft.set_color_by_gradient(BLUE, PURPLE, ORANGE, WHITE)

        # Animate the curve drawing from left to right
        self.play(
            Create(glow_soft),
            run_time=2.5,
            rate_func=smooth
        )

        self.play(
            Create(glow),
            Create(curve),
            run_time=2.5,
            rate_func=smooth
        )

        self.wait(1)

        # ===== COMMIT 3: STAGE 1 - PARTICLES/ATOMS =====

        # Define position on curve for atoms (early stage, low complexity)
        atoms_x = 1.5
        atoms_y = complexity_curve(atoms_x)
        atoms_point = axes.coords_to_point(atoms_x, atoms_y)

        # Create a marker dot on the curve
        stage_marker = Dot(atoms_point, color=BLUE, radius=0.1)
        self.play(FadeIn(stage_marker), run_time=0.5)
        self.wait(0.3)

        # Create small particles appearing randomly around the marker
        num_particles = 12
        particles = VGroup()

        for i in range(num_particles):
            # Random offset around the marker point
            offset_x = np.random.uniform(-0.8, 0.8)
            offset_y = np.random.uniform(-0.8, 0.8)
            particle_pos = atoms_point + RIGHT * offset_x + UP * offset_y

            particle = Dot(
                particle_pos,
                color=BLUE_C,
                radius=0.06
            )
            particles.add(particle)

        # Animate particles appearing with random motion
        self.play(
            LaggedStart(
                *[FadeIn(p, shift=UP * 0.2) for p in particles],
                lag_ratio=0.1
            ),
            run_time=1.5
        )

        # Add slight random motion to particles
        particle_animations = []
        for p in particles:
            new_pos = p.get_center() + RIGHT * np.random.uniform(-0.3, 0.3) + UP * np.random.uniform(-0.3, 0.3)
            particle_animations.append(p.animate.move_to(new_pos))

        self.play(*particle_animations, run_time=1, rate_func=there_and_back)

        # Group particles together at the marker
        self.play(
            *[p.animate.move_to(atoms_point) for p in particles],
            run_time=1.5,
            rate_func=smooth
        )

        # Fade out all but one particle
        particles_to_fade = particles[1:]
        self.play(
            *[FadeOut(p) for p in particles_to_fade],
            run_time=0.8
        )

        # Zoom in on the remaining particle (transform into atom)
        single_particle = particles[0]

        # Create atom structure: nucleus + electron orbits
        nucleus = Dot(atoms_point, color=BLUE_B, radius=0.12)

        # Create electron orbits (2 orbits with electrons)
        orbit1 = Circle(radius=0.4, color=BLUE_C, stroke_width=1.5, stroke_opacity=0.6)
        orbit1.move_to(atoms_point)

        orbit2 = Circle(radius=0.65, color=BLUE_C, stroke_width=1.5, stroke_opacity=0.6)
        orbit2.move_to(atoms_point)
        orbit2.rotate(PI / 3)  # Tilted orbit

        # Electrons on orbits
        electron1 = Dot(orbit1.point_from_proportion(0), color=BLUE_A, radius=0.08)
        electron2 = Dot(orbit2.point_from_proportion(0.5), color=BLUE_A, radius=0.08)

        atom_structure = VGroup(orbit1, orbit2, nucleus, electron1, electron2)

        # Transform particle into atom
        self.play(
            ReplacementTransform(single_particle, nucleus),
            FadeIn(orbit1),
            FadeIn(orbit2),
            FadeIn(electron1),
            FadeIn(electron2),
            run_time=1.5
        )

        # Animate electrons orbiting
        def update_electron1(mob, dt):
            mob.rotate(2 * dt, about_point=atoms_point)

        def update_electron2(mob, dt):
            mob.rotate(-1.5 * dt, about_point=atoms_point)

        electron1.add_updater(update_electron1)
        electron2.add_updater(update_electron2)

        self.wait(1.5)

        # Add "Atoms" label
        atoms_label = Text("Atoms", font_size=28, color=BLUE_C)
        atoms_label.next_to(atoms_point, RIGHT + DOWN, buff=0.5)

        # Add a small line connecting label to the point
        label_line = Line(
            atoms_point,
            atoms_label.get_corner(UP + LEFT),
            color=BLUE_C,
            stroke_width=1.5,
            stroke_opacity=0.6
        )

        self.play(
            Create(label_line),
            Write(atoms_label),
            run_time=1
        )

        self.wait(1.5)

        # Remove electron updaters and fade out atom for next stage
        electron1.remove_updater(update_electron1)
        electron2.remove_updater(update_electron2)

        self.wait(1)
