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

        self.wait(2)
