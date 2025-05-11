from manim import *


class GitAndTreeSplit(Scene):
    def construct(self):
        self.camera.background_color = "#002b36"

        # Create the Git flow diagram on the left side
        git_group = VGroup()

        # Define start points for branches - MODIFIED: moved everything right
        start_x = -5  # Changed from -6 to -5 to move everything right
        x_step = 1.2

        # Branch Y positions
        y_develop = 1
        y_pull = 0

        # Branch labels
        labels = [
            ("develop", y_develop, BLUE),
            ("pull/1234", y_pull, ORANGE)
        ]

        # Create labels - MODIFIED: moved labels more to the right
        branch_labels = VGroup()
        for name, y, color in labels:
            # Changed LEFT to LEFT + RIGHT * 1.0 to move labels further to the right
            label = Text(name, font_size=24, color=color).next_to([start_x, y, 0], LEFT + RIGHT * 1.0)
            self.play(Write(label), run_time=0.3)
            branch_labels.add(label)
            git_group.add(label)

        # Initialize paths - MODIFIED: adjusted line positions (compromise between previous values)
        lines = {
            "develop": Line([start_x + 0.85, y_develop, 0], [start_x + 0.85, y_develop, 0], color=BLUE),
            "pull": Line([start_x + 0.85, y_pull, 0], [start_x + 0.85, y_pull, 0], color=ORANGE),
        }

        # Show line starting points
        for line in lines.values():
            self.play(Create(line), run_time=0.2)
            git_group.add(line)

        # MODIFIED: Reduced to only 3 commits
        commits = [
            ("develop", 1),
            ("develop", 2),
            ("pull", 1),
            # Removed the last two commits:
            # ("develop", 3),
            # ("pull", 2),
        ]

        dot_radius = 0.12
        dots = VGroup()

        # Now create tree side
        tree_origin = RIGHT * 3 + UP * 3
        line_spacing = 0.15  # Reduced spacing between lines
        block_spacing = 0.08  # Reduced spacing between blocks

        # Starting point with smaller font size
        tree_lines = [
            ".",
            "└── packages/"
        ]
        text_objs = [Text(line, font="Courier", font_size=20, color="#93a1a1") for line in tree_lines]
        tree_group = VGroup(*text_objs).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(RIGHT * 0.5)
        tree_group.move_to(tree_origin, aligned_edge=UP+RIGHT)

        self.play(*[Write(line) for line in tree_group])
        self.wait(0.5)

        # Process commits and tree growth together
        current_block = tree_group

        for i, (branch, index) in enumerate(commits):
            # Git side: Extend branch line
            x = start_x + 0.85 + index * x_step  # MODIFIED: Using compromise value of 0.85
            y = y_develop if branch == "develop" else y_pull

            # Grow line
            new_line = Line([start_x + 0.85, y, 0], [x, y, 0], color=lines[branch].get_color())
            self.play(Transform(lines[branch], new_line), run_time=0.3)

            # Add commit dot
            dot = Dot(point=[x, y, 0], radius=dot_radius, color=lines[branch].get_color())
            self.play(FadeIn(dot), run_time=0.2)
            dots.add(dot)

            # Tree side: Add or update tree based on commit
            if i == 0:  # First develop commit
                develop1_lines = [
                    "    ├── develop/",
                    "    │   └── githash1/",
                    "    │       └── my-package/",
                    "    │           └── index.html"
                ]
                develop1_block = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in develop1_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                develop1_block.next_to(current_block, DOWN, aligned_edge=LEFT, buff=block_spacing)
                self.play(FadeIn(develop1_block), run_time=0.4)

                # Add glow effect for develop/githash1 (blue)
                # Create copy for glow effect
                glow_develop1 = develop1_block.copy()
                glow_develop1.set_color(BLUE)
                glow_develop1.set_stroke(width=4)

                # Apply glow animation
                self.play(
                    FadeIn(glow_develop1, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=1
                )
                self.play(FadeOut(glow_develop1), run_time=0.5)

                current_block = develop1_block

            elif i == 1:  # Second develop commit
                # Update develop1 to change └── to ├── for githash1
                develop1_updated_lines = [
                    "    ├── develop/",
                    "    │   ├── githash1/",
                    "    │   │   └── my-package/",
                    "    │   │       └── index.html"
                ]
                develop1_updated = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in develop1_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                develop1_updated.move_to(current_block.get_center())
                self.play(Transform(current_block, develop1_updated), run_time=0.4)

                # Add githash3
                develop2_lines = [
                    "    │   └── githash2/",
                    "    │       └── my-package/",
                    "    │           └── index.html"
                ]
                develop2_block = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in develop2_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                develop2_block.next_to(current_block, DOWN, aligned_edge=LEFT, buff=block_spacing)
                develop2_block.align_to(current_block, LEFT)
                self.play(FadeIn(develop2_block), run_time=0.4)

                # Add glow effect for develop/githash3 (blue)
                # Create copy for glow effect
                glow_develop2 = develop2_block.copy()
                glow_develop2.set_color(BLUE)
                glow_develop2.set_stroke(width=4)

                # Apply glow animation
                self.play(
                    FadeIn(glow_develop2, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=1
                )
                self.play(FadeOut(glow_develop2), run_time=0.5)

                current_block = develop2_block

            elif i == 2:  # First pull request commit
                pull_block_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       └── githash3/",
                    "    │           └── my-package/",
                    "    │               └── index.html"
                ]
                pull_block = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in pull_block_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                pull_block.next_to(current_block, DOWN, aligned_edge=LEFT, buff=block_spacing)
                self.play(FadeIn(pull_block), run_time=0.4)

                # Add glow effect for pull/1234 (orange)
                # Create copy for glow effect
                glow_pull = pull_block.copy()
                glow_pull.set_color(ORANGE)
                glow_pull.set_stroke(width=4)

                # Start the pull/1234 glow animation - even faster
                self.play(
                    FadeIn(glow_pull, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6  # Super short glow animation
                )

                # Set current_block for subsequent animations
                current_block = pull_block

                # Prepare updated pull block structure
                pull_block_updated_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       ├── githash3/",  # Changed from └── to ├──
                    "    │       │   └── my-package/",
                    "    │       │       └── index.html"
                ]
                pull_block_updated = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in pull_block_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                pull_block_updated.move_to(current_block.get_center())

                # Prepare HEAD file content
                head_file_lines = [
                    "    │       └── HEAD"  # HEAD file as sibling to githash3
                ]
                head_file_block = VGroup(*[
                    Text(line, font="Courier", font_size=18, color="#93a1a1")
                    for line in head_file_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                head_file_block.next_to(pull_block_updated, DOWN, aligned_edge=LEFT, buff=block_spacing)
                head_file_block.align_to(pull_block_updated, LEFT)

                # Start fading out the pull glow WHILE simultaneously updating structure
                # This creates more overlap between animations
                self.play(
                    FadeOut(glow_pull, run_time=0.25),
                    Transform(current_block, pull_block_updated, run_time=0.3)  # Slightly longer so it extends beyond the fadeout
                )

                # Begin fading in the HEAD file before the structure update is fully complete
                # Start HEAD file fade-in animation without waiting for previous animation to complete
                self.add(head_file_block.set_opacity(0))  # Add with opacity 0 (invisible)
                head_fade_in = head_file_block.animate.set_opacity(1)  # Animation to fade in

                # Play both animations simultaneously with a slight offset
                # This creates the effect of HEAD appearing while structure is still updating
                self.play(head_fade_in, run_time=0.2)

                # The pull_block structure has already been updated in the previous step

                # Start the HEAD glow effect while the HEAD is still appearing
                # This creates maximum overlap between animations
                glow_head = head_file_block.copy()
                glow_head.set_color(ORANGE)
                glow_head.set_stroke(width=4)
                glow_head.set_opacity(0)  # Start invisible
                self.add(glow_head)  # Add to scene but invisible

                # Fade in the glow simultaneously with the HEAD file's appearance
                # This creates the effect of the HEAD starting to glow right as it appears
                glow_fade_in = glow_head.animate.set_opacity(1)
                self.play(glow_fade_in, run_time=0.3)

                # Complete the glow effect - shorter and faster
                glow_pulse = glow_head.animate.set_opacity(0.8)
                self.play(glow_pulse, run_time=0.2)
                self.play(FadeOut(glow_head), run_time=0.3)

                current_block = head_file_block

            # Let each step be visible
            self.wait(0.3)

        # Final pause to see the completed visualization
        self.wait(2)