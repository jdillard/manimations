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
                
                # Apply glow animation
                self.play(
                    FadeIn(glow_pull, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=1
                )
                self.play(FadeOut(glow_pull), run_time=0.5)
                
                current_block = pull_block
            
            # Let each step be visible
            self.wait(0.3)
        
        # Final pause to see the completed visualization
        self.wait(2)