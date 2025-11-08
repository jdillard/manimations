from manim import *

class ComplexityConsciousness(Scene):
    def construct(self):
        # ===== COMMIT 10: FINAL POLISH =====
        # High quality render settings applied via command line:
        # For 1080p60: manim -pqh --fps 60 complexity-consciousness/main.py ComplexityConsciousness
        # Duration: ~75 seconds (60-90 second target met)

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

        # Add subtitle explanation (COMMIT 10)
        atoms_subtitle = Text(
            "Elementary particles organize into stable atomic structures",
            font_size=20,
            color=BLUE_C,
            opacity=0.7
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(label_line),
            Write(atoms_label),
            FadeIn(atoms_subtitle, shift=UP * 0.2),
            run_time=1
        )

        self.wait(1.5)

        # Remove electron updaters and fade out atom for next stage
        electron1.remove_updater(update_electron1)
        electron2.remove_updater(update_electron2)

        self.wait(0.5)

        # ===== COMMIT 4: STAGE 2 - MOLECULES =====

        # Define position on curve for molecules (higher complexity)
        molecules_x = 3.5
        molecules_y = complexity_curve(molecules_x)
        molecules_point = axes.coords_to_point(molecules_x, molecules_y)

        # Create new stage marker
        molecules_marker = Dot(molecules_point, color=PURPLE, radius=0.1)

        # Fade out atom structure and move marker to new position
        self.play(
            stage_marker.animate.move_to(molecules_point).set_color(PURPLE),
            FadeOut(atom_structure),
            FadeOut(atoms_label),
            FadeOut(label_line),
            FadeOut(atoms_subtitle),
            run_time=1.5
        )

        self.wait(0.5)

        # Create simple molecule structure (like water - 3 atoms bonded)
        # Central atom
        center_atom = Dot(molecules_point, color=PURPLE_B, radius=0.15)

        # Side atoms
        atom_left = Dot(molecules_point + LEFT * 0.5 + UP * 0.3, color=PURPLE_C, radius=0.12)
        atom_right = Dot(molecules_point + RIGHT * 0.5 + UP * 0.3, color=PURPLE_C, radius=0.12)

        # Bonds (lines connecting atoms)
        bond_left = Line(
            center_atom.get_center(),
            atom_left.get_center(),
            color=PURPLE,
            stroke_width=3
        )
        bond_right = Line(
            center_atom.get_center(),
            atom_right.get_center(),
            color=PURPLE,
            stroke_width=3
        )

        simple_molecule = VGroup(bond_left, bond_right, center_atom, atom_left, atom_right)

        # Animate atoms appearing and bonds forming
        self.play(
            FadeIn(center_atom),
            FadeIn(atom_left),
            FadeIn(atom_right),
            run_time=1
        )

        self.play(
            Create(bond_left),
            Create(bond_right),
            run_time=1
        )

        self.wait(0.5)

        # Transform into DNA double helix
        # Create DNA helix using parametric curves
        def helix1(t):
            return molecules_point + RIGHT * 0.3 * np.cos(2 * PI * t) + UP * (t - 0.5) * 1.5

        def helix2(t):
            return molecules_point + RIGHT * 0.3 * np.cos(2 * PI * t + PI) + UP * (t - 0.5) * 1.5

        # Create the two strands
        strand1 = ParametricFunction(
            helix1,
            t_range=[0, 1],
            color=PURPLE_B,
            stroke_width=3
        )

        strand2 = ParametricFunction(
            helix2,
            t_range=[0, 1],
            color=PURPLE_C,
            stroke_width=3
        )

        # Create base pairs (rungs connecting the two strands)
        num_rungs = 5
        rungs = VGroup()
        for i in range(num_rungs):
            t = i / (num_rungs - 1)
            point1 = helix1(t)
            point2 = helix2(t)
            rung = Line(point1, point2, color=PURPLE, stroke_width=2, stroke_opacity=0.6)
            rungs.add(rung)

        dna_helix = VGroup(strand1, strand2, rungs)

        # Transform simple molecule into DNA
        self.play(
            FadeOut(simple_molecule),
            run_time=0.5
        )

        self.play(
            Create(strand1),
            Create(strand2),
            run_time=2,
            rate_func=smooth
        )

        self.play(
            LaggedStart(
                *[Create(rung) for rung in rungs],
                lag_ratio=0.2
            ),
            run_time=1.5
        )

        self.wait(1)

        # Add "Molecules" label
        molecules_label = Text("Molecules", font_size=28, color=PURPLE)
        molecules_label.next_to(molecules_point, RIGHT, buff=0.7)

        # Label line
        molecules_label_line = Line(
            molecules_point,
            molecules_label.get_corner(LEFT),
            color=PURPLE,
            stroke_width=1.5,
            stroke_opacity=0.6
        )

        # Add subtitle explanation (COMMIT 10)
        molecules_subtitle = Text(
            "Atoms bond to form complex molecules - the building blocks of life",
            font_size=20,
            color=PURPLE,
            opacity=0.7
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(molecules_label_line),
            Write(molecules_label),
            FadeIn(molecules_subtitle, shift=UP * 0.2),
            run_time=1
        )

        self.wait(1)

        # ===== COMMIT 5: STAGE 3 - CELLS =====

        # Define position on curve for cells (even higher complexity)
        cells_x = 5.5
        cells_y = complexity_curve(cells_x)
        cells_point = axes.coords_to_point(cells_x, cells_y)

        # Move marker to new position and fade out DNA
        self.play(
            stage_marker.animate.move_to(cells_point).set_color(ORANGE),
            FadeOut(dna_helix),
            FadeOut(molecules_label),
            FadeOut(molecules_label_line),
            FadeOut(molecules_subtitle),
            run_time=1.5
        )

        self.wait(0.5)

        # Create cell membrane (outer circle)
        cell_membrane = Circle(
            radius=0.8,
            color=ORANGE,
            stroke_width=3,
            fill_opacity=0.05,
            fill_color=ORANGE
        ).move_to(cells_point)

        # Create nucleus (large central organelle)
        cell_nucleus = Circle(
            radius=0.25,
            color=ORANGE,
            stroke_width=2,
            fill_opacity=0.3,
            fill_color=ORANGE
        ).move_to(cells_point)

        # Create mitochondria (smaller oval organelles)
        mitochondria1 = Ellipse(
            width=0.3,
            height=0.15,
            color=RED_E,
            stroke_width=1.5,
            fill_opacity=0.25,
            fill_color=RED_E
        ).move_to(cells_point + UP * 0.35 + LEFT * 0.2)

        mitochondria2 = Ellipse(
            width=0.3,
            height=0.15,
            color=RED_E,
            stroke_width=1.5,
            fill_opacity=0.25,
            fill_color=RED_E
        ).move_to(cells_point + DOWN * 0.3 + RIGHT * 0.25).rotate(PI / 4)

        # Additional small organelles (vesicles)
        vesicle1 = Dot(
            cells_point + UP * 0.2 + RIGHT * 0.3,
            color=YELLOW_E,
            radius=0.06
        )

        vesicle2 = Dot(
            cells_point + DOWN * 0.15 + LEFT * 0.35,
            color=YELLOW_E,
            radius=0.06
        )

        cell_organelles = VGroup(cell_nucleus, mitochondria1, mitochondria2, vesicle1, vesicle2)

        # Animate cell appearing
        self.play(
            Create(cell_membrane),
            run_time=1.5
        )

        # Animate organelles appearing
        self.play(
            FadeIn(cell_nucleus),
            run_time=0.8
        )

        self.play(
            LaggedStart(
                FadeIn(mitochondria1),
                FadeIn(mitochondria2),
                FadeIn(vesicle1),
                FadeIn(vesicle2),
                lag_ratio=0.3
            ),
            run_time=1.5
        )

        self.wait(0.5)

        # Create pulsing/breathing animation for cell membrane
        # Use simple scale animations for the pulsing effect
        self.play(
            cell_membrane.animate.scale(1.08),
            cell_organelles.animate.scale(1.04),
            run_time=1.5,
            rate_func=there_and_back
        )

        self.play(
            cell_membrane.animate.scale(1.08),
            cell_organelles.animate.scale(1.04),
            run_time=1.5,
            rate_func=there_and_back
        )

        # Add "Cells" label
        cells_label = Text("Cells", font_size=28, color=ORANGE)
        cells_label.next_to(cells_point, RIGHT + DOWN, buff=0.6)

        # Label line
        cells_label_line = Line(
            cells_point + RIGHT * 0.8,
            cells_label.get_corner(UP + LEFT),
            color=ORANGE,
            stroke_width=1.5,
            stroke_opacity=0.6
        )

        # Add subtitle explanation (COMMIT 10)
        cells_subtitle = Text(
            "Molecules organize into living cells with internal structure and metabolism",
            font_size=20,
            color=ORANGE,
            opacity=0.7
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(cells_label_line),
            Write(cells_label),
            FadeIn(cells_subtitle, shift=UP * 0.2),
            run_time=1
        )

        # Continue pulsing effect
        self.play(
            cell_membrane.animate.scale(1.08),
            cell_organelles.animate.scale(1.04),
            run_time=1.5,
            rate_func=there_and_back
        )

        self.wait(0.5)

        # ===== COMMIT 6: STAGE 4 - ORGANISMS =====

        # Define position on curve for organisms (higher complexity)
        organisms_x = 7.0
        organisms_y = complexity_curve(organisms_x)
        organisms_point = axes.coords_to_point(organisms_x, organisms_y)

        # Move marker to new position and fade out cell
        self.play(
            stage_marker.animate.move_to(organisms_point).set_color(RED),
            FadeOut(cell_membrane),
            FadeOut(cell_organelles),
            FadeOut(cells_label),
            FadeOut(cells_label_line),
            FadeOut(cells_subtitle),
            run_time=1.5
        )

        self.wait(0.5)

        # Create multiple cells forming a network
        num_cells = 6
        cell_positions = [
            organisms_point + UP * 0.6,
            organisms_point + DOWN * 0.6,
            organisms_point + LEFT * 0.7 + UP * 0.3,
            organisms_point + RIGHT * 0.7 + UP * 0.3,
            organisms_point + LEFT * 0.7 + DOWN * 0.3,
            organisms_point + RIGHT * 0.7 + DOWN * 0.3,
        ]

        cells_network = VGroup()
        for pos in cell_positions:
            cell = Circle(
                radius=0.25,
                color=RED,
                stroke_width=2,
                fill_opacity=0.1,
                fill_color=RED
            ).move_to(pos)
            cells_network.add(cell)

        # Animate cells appearing
        self.play(
            LaggedStart(
                *[FadeIn(cell) for cell in cells_network],
                lag_ratio=0.15
            ),
            run_time=2
        )

        self.wait(0.5)

        # Create nervous system as branching network
        # Central node (brain representation)
        brain_node = Circle(
            radius=0.15,
            color=YELLOW,
            stroke_width=2,
            fill_opacity=0.4,
            fill_color=YELLOW
        ).move_to(organisms_point + UP * 0.6)

        # Neural connections between cells
        neural_connections = VGroup()
        connection_pairs = [
            (0, 2), (0, 3), (1, 4), (1, 5),  # From top and bottom cells
            (2, 4), (3, 5), (2, 3), (4, 5),  # Cross connections
        ]

        for i, j in connection_pairs:
            line = Line(
                cell_positions[i],
                cell_positions[j],
                color=YELLOW,
                stroke_width=2,
                stroke_opacity=0.6
            )
            neural_connections.add(line)

        # Show nervous system emerging
        self.play(
            FadeIn(brain_node),
            run_time=0.8
        )

        self.play(
            LaggedStart(
                *[Create(line) for line in neural_connections],
                lag_ratio=0.1
            ),
            run_time=2
        )

        self.wait(0.5)

        # Create firing/pulsing neural signals
        # Create dots that travel along connections
        signal_dots = VGroup()
        for line in neural_connections[:4]:  # Use first 4 connections
            dot = Dot(
                line.get_start(),
                color=YELLOW,
                radius=0.08
            )
            signal_dots.add(dot)

        self.play(
            *[FadeIn(dot) for dot in signal_dots],
            run_time=0.3
        )

        # Animate signals traveling along connections
        signal_animations = []
        for i, dot in enumerate(signal_dots):
            line = neural_connections[i]
            signal_animations.append(
                dot.animate.move_to(line.get_end())
            )

        self.play(
            *signal_animations,
            run_time=1.5,
            rate_func=smooth
        )

        # Fade out and repeat with different connections
        self.play(
            *[FadeOut(dot) for dot in signal_dots],
            run_time=0.3
        )

        # Second wave of signals
        signal_dots_2 = VGroup()
        for line in neural_connections[4:]:  # Use remaining connections
            dot = Dot(
                line.get_start(),
                color=YELLOW,
                radius=0.08
            )
            signal_dots_2.add(dot)

        self.play(
            *[FadeIn(dot) for dot in signal_dots_2],
            run_time=0.3
        )

        signal_animations_2 = []
        for i, dot in enumerate(signal_dots_2):
            line = neural_connections[i + 4]
            signal_animations_2.append(
                dot.animate.move_to(line.get_end())
            )

        self.play(
            *signal_animations_2,
            run_time=1.5,
            rate_func=smooth
        )

        self.play(
            *[FadeOut(dot) for dot in signal_dots_2],
            run_time=0.3
        )

        # Add "Organisms" label
        organisms_label = Text("Organisms", font_size=28, color=RED)
        organisms_label.next_to(organisms_point, RIGHT, buff=0.8)

        # Label line
        organisms_label_line = Line(
            organisms_point,
            organisms_label.get_corner(LEFT),
            color=RED,
            stroke_width=1.5,
            stroke_opacity=0.6
        )

        # Add subtitle explanation (COMMIT 10)
        organisms_subtitle = Text(
            "Cells unite to form organisms with nervous systems and conscious awareness",
            font_size=20,
            color=RED,
            opacity=0.7
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(organisms_label_line),
            Write(organisms_label),
            FadeIn(organisms_subtitle, shift=UP * 0.2),
            run_time=1
        )

        self.wait(1)

        # ===== COMMIT 7: STAGE 5 - NOOSPHERE =====

        # Define position on curve for noosphere (very high complexity)
        noosphere_x = 8.5
        noosphere_y = complexity_curve(noosphere_x)
        noosphere_point = axes.coords_to_point(noosphere_x, noosphere_y)

        # Move marker to new position and fade out organisms
        self.play(
            stage_marker.animate.move_to(noosphere_point).set_color(GOLD),
            FadeOut(cells_network),
            FadeOut(brain_node),
            FadeOut(neural_connections),
            FadeOut(organisms_label),
            FadeOut(organisms_label_line),
            FadeOut(organisms_subtitle),
            run_time=1.5
        )

        self.wait(0.5)

        # Create small Earth at center
        earth = Circle(
            radius=0.3,
            color=BLUE,
            stroke_width=2,
            fill_opacity=0.3,
            fill_color=BLUE
        ).move_to(noosphere_point)

        # Add simple continents/texture to Earth
        earth_detail1 = Arc(
            radius=0.25,
            angle=PI/2,
            color=GREEN,
            stroke_width=1.5
        ).move_to(noosphere_point + UP * 0.1 + LEFT * 0.05)

        earth_detail2 = Dot(
            noosphere_point + DOWN * 0.15 + RIGHT * 0.1,
            color=GREEN,
            radius=0.08
        )

        earth_group = VGroup(earth, earth_detail1, earth_detail2)

        self.play(
            FadeIn(earth_group),
            run_time=1
        )

        self.wait(0.5)

        # Create brain/head silhouettes around Earth
        num_brains = 8
        brain_radius = 1.2  # Distance from center
        brains = VGroup()

        for i in range(num_brains):
            angle = i * 2 * PI / num_brains
            pos = noosphere_point + RIGHT * brain_radius * np.cos(angle) + UP * brain_radius * np.sin(angle)

            # Simple brain silhouette (circle with a small detail)
            brain_circle = Circle(
                radius=0.15,
                color=WHITE,
                stroke_width=2,
                fill_opacity=0.2,
                fill_color=WHITE
            ).move_to(pos)

            brains.add(brain_circle)

        # Animate brains appearing
        self.play(
            LaggedStart(
                *[FadeIn(brain, scale=0.5) for brain in brains],
                lag_ratio=0.1
            ),
            run_time=2
        )

        self.wait(0.5)

        # Create dense network of connections between brains
        connections = VGroup()

        # Connect each brain to multiple others
        for i in range(num_brains):
            # Connect to next 3 brains in the circle
            for j in range(1, 4):
                next_idx = (i + j) % num_brains
                line = Line(
                    brains[i].get_center(),
                    brains[next_idx].get_center(),
                    color=GOLD,
                    stroke_width=1.5,
                    stroke_opacity=0.5
                )
                connections.add(line)

        # Add connections from brains to Earth (collective consciousness)
        earth_connections = VGroup()
        for brain in brains:
            line = Line(
                brain.get_center(),
                noosphere_point,
                color=YELLOW,
                stroke_width=1,
                stroke_opacity=0.3
            )
            earth_connections.add(line)

        # Animate network forming
        self.play(
            LaggedStart(
                *[Create(line) for line in earth_connections],
                lag_ratio=0.05
            ),
            run_time=2
        )

        self.play(
            LaggedStart(
                *[Create(line) for line in connections],
                lag_ratio=0.02
            ),
            run_time=2.5
        )

        self.wait(0.5)

        # Create sphere around the network (noosphere boundary)
        noosphere_sphere = Circle(
            radius=brain_radius + 0.3,
            color=GOLD,
            stroke_width=2,
            stroke_opacity=0.6
        ).move_to(noosphere_point)

        # Create a subtle glow around the sphere
        sphere_glow = Circle(
            radius=brain_radius + 0.4,
            color=WHITE,
            stroke_width=4,
            stroke_opacity=0.3
        ).move_to(noosphere_point)

        self.play(
            Create(sphere_glow),
            Create(noosphere_sphere),
            run_time=2,
            rate_func=smooth
        )

        # Pulse the entire noosphere
        self.play(
            noosphere_sphere.animate.scale(1.1),
            sphere_glow.animate.scale(1.1),
            run_time=1,
            rate_func=there_and_back
        )

        # Add "Noosphere" label
        noosphere_label = Text("Noosphere", font_size=28, color=GOLD)
        noosphere_label.next_to(noosphere_point, DOWN, buff=1.8)

        # Label line
        noosphere_label_line = Line(
            noosphere_point + DOWN * (brain_radius + 0.3),
            noosphere_label.get_top(),
            color=GOLD,
            stroke_width=1.5,
            stroke_opacity=0.6
        )

        # Add subtitle explanation (COMMIT 10)
        noosphere_subtitle = Text(
            "Humanity forms a planetary sphere of collective consciousness and thought",
            font_size=20,
            color=GOLD,
            opacity=0.7
        ).to_edge(DOWN, buff=0.3)

        self.play(
            Create(noosphere_label_line),
            Write(noosphere_label),
            FadeIn(noosphere_subtitle, shift=UP * 0.2),
            run_time=1
        )

        # Final pulse showing the living noosphere
        self.play(
            noosphere_sphere.animate.scale(1.08),
            sphere_glow.animate.scale(1.08),
            run_time=1.5,
            rate_func=there_and_back
        )

        self.wait(1)

        # ===== COMMIT 9: SMOOTH TRANSITIONS & TIMING =====

        # Slowly zoom out to show the complete evolutionary journey
        # Group everything for the final zoom out
        everything = VGroup(
            grid, axes, x_label, y_label, title,
            glow_soft, glow, curve,
            stage_marker,
            earth_group, brains, earth_connections, connections,
            noosphere_sphere, sphere_glow,
            noosphere_label, noosphere_label_line
        )

        # Zoom out smoothly to reveal the full journey
        self.play(
            everything.animate.scale(0.88).shift(DOWN * 0.25),
            FadeOut(noosphere_subtitle),
            run_time=4,
            rate_func=smooth
        )

        self.wait(0.5)

        # Final celebratory pulse of the noosphere
        self.play(
            noosphere_sphere.animate.scale(1.12),
            sphere_glow.animate.scale(1.12),
            run_time=2,
            rate_func=there_and_back
        )

        self.wait(2)
