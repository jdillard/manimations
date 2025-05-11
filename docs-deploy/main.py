from manim import *

"""
This animation demonstrates the relationship between Git branches and their
corresponding documentation file system structure. It shows:

1. A Git repository visualization on the left with branches (develop and a pull request)
2. A concurrent file system tree visualization on the right showing how the commits
   and tags structured directory hierarchy gets deployed
3. How HEAD reference is updated to track the latest commit in each branch
4. How tags are stored in the file system

This visualization helps understand the connection between Git's branching
model and deployed file structure of the docs.
"""


class GitAndTreeSplit(Scene):
    def construct(self):
        # Set the background color to Solarized Dark theme
        self.camera.background_color = "#002b36"

        # Create the Git flow diagram on the left side
        git_group = VGroup()

        # Define starting positions for branches
        start_x = -5
        x_step = 1.2

        # Define Y-positions for each branch
        y_develop = 1
        y_pull = 0

        # Define branch labels with name, position, and color
        labels = [
            ("develop", y_develop, BLUE),
            ("pull/1234", y_pull, ORANGE)
        ]

        # Create and animate branch labels
        branch_labels = VGroup()
        for name, y, color in labels:
            label = Text(name, font_size=24, color=color).next_to([start_x, y, 0], LEFT + RIGHT * 1.0)
            self.play(Write(label), run_time=0.3)
            branch_labels.add(label)
            git_group.add(label)

        # Initialize branch lines (initially with zero length)
        lines = {
            "develop": Line([start_x + 0.85, y_develop, 0], [start_x + 0.85, y_develop, 0], color=BLUE),
            "pull": Line([start_x + 0.85, y_pull, 0], [start_x + 0.85, y_pull, 0], color=ORANGE),
        }

        # Create initial branch line endpoints
        for line in lines.values():
            self.play(Create(line), run_time=0.2)
            git_group.add(line)

        # Define commit sequence: format is (branch_name, commit_number)
        commits = [
            ("develop", 1),
            ("develop", 2),
            ("pull", 1),
        ]

        # Define which commit will be tagged
        tag_commit = ("develop", 2)  # Tag the second develop commit as v1.0.0

        # Set commit dot size
        dot_radius = 0.12
        dots = VGroup()

        # Setup the directory tree visualization on the right side
        tree_origin = RIGHT * 2.5 + UP * 3.5  # Position for better vertical centering
        line_spacing = 0.15  # Spacing between tree lines
        block_spacing = 0.08  # Spacing between directory blocks

        # Initial tree structure
        tree_lines = [
            ".",
            "└── modules/"
        ]

        # Create the root tree structure
        text_objs = [Text(line, font="Courier", font_size=18, color="#93a1a1") for line in tree_lines]
        tree_group = VGroup(*text_objs).arrange(DOWN, aligned_edge=LEFT)

        # Position the tree at its origin point
        tree_group.move_to(tree_origin, aligned_edge=UP+RIGHT)

        # Show the initial tree structure
        self.play(*[Write(line) for line in tree_group])
        self.wait(0.5)

        # Calculate reference point for consistent indentation
        root_line = text_objs[1]  # "└── modules/" line
        p_index = 4  # Position of 'p' in "modules/" (0-indexed)
        p_position = root_line.get_left() + RIGHT * p_index * root_line.width / len("└── modules/")

        # Initialize variables to track tree blocks
        current_block = tree_group
        head_block = None
        last_develop_block = None

        # Process each commit and grow the tree correspondingly
        for i, (branch, index) in enumerate(commits):
            # Git side: Extend the branch line for the new commit
            x = start_x + 0.85 + index * x_step
            y = y_develop if branch == "develop" else y_pull

            # Animate branch line growth
            new_line = Line([start_x + 0.85, y, 0], [x, y, 0], color=lines[branch].get_color())
            self.play(Transform(lines[branch], new_line), run_time=0.3)

            # Add commit dot
            dot = Dot(point=[x, y, 0], radius=dot_radius, color=lines[branch].get_color())
            self.play(FadeIn(dot), run_time=0.2)
            dots.add(dot)

            # Tree side: Update file system based on the commit
            if i == 0:  # First develop commit
                # Create directory structure for first develop commit
                develop1_lines = [
                    "    ├── develop/",
                    "    │   └── githash1/",
                    "    │       └── module1/",
                    "    │           └── index.html"
                ]
                develop1_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in develop1_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the directory block with proper indentation
                develop1_block.next_to(current_block, DOWN, buff=block_spacing)
                develop1_block.align_to(p_position, LEFT)

                # Show the new directory structure
                self.play(FadeIn(develop1_block), run_time=0.4)
                last_develop_block = develop1_block

                # Add highlight effect for new commit directory
                glow_develop1 = develop1_block.copy()
                glow_develop1.set_color(BLUE)
                glow_develop1.set_stroke(width=4)

                # Animate the highlight
                self.play(
                    FadeIn(glow_develop1, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )

                # Update tree structure to prepare for next commit
                # Change └── to ├── for githash1 to indicate more commits coming
                develop1_updated_lines = [
                    "    ├── develop/",
                    "    │   ├── githash1/",  # Changed from └── to ├──
                    "    │   │   └── module1/",
                    "    │   │       └── index.html"
                ]
                develop1_updated = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in develop1_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Maintain correct positioning
                develop1_updated.move_to(develop1_block.get_center())
                develop1_updated.align_to(develop1_block, LEFT)

                # Add HEAD file to track current branch position
                develop_head_lines = [
                    "    │   └── HEAD"  # HEAD file as sibling to githash1
                ]
                head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in develop_head_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position HEAD file
                head_block.next_to(develop1_updated, DOWN, aligned_edge=LEFT, buff=block_spacing)
                head_block.align_to(develop1_updated, LEFT)

                # Update directory structure and add HEAD file
                self.play(
                    FadeOut(glow_develop1, run_time=0.25),
                    Transform(develop1_block, develop1_updated, run_time=0.3)
                )

                # Show the HEAD file appearing
                self.add(head_block.set_opacity(0))
                head_fade_in = head_block.animate.set_opacity(1)
                self.play(head_fade_in, run_time=0.2)

                # Highlight the HEAD file to show it's important
                glow_develop_head = head_block.copy()
                glow_develop_head.set_color(BLUE)
                glow_develop_head.set_stroke(width=4)
                glow_develop_head.set_opacity(0)
                self.add(glow_develop_head)

                # Animate the HEAD highlight
                glow_fade_in = glow_develop_head.animate.set_opacity(1)
                self.play(glow_fade_in, run_time=0.3)
                glow_pulse = glow_develop_head.animate.set_opacity(0.8)
                self.play(glow_pulse, run_time=0.2)
                self.play(FadeOut(glow_develop_head), run_time=0.3)

                current_block = head_block
                last_develop_block = develop1_block

            elif i == 1:  # Second develop commit
                # Create directory structure for second develop commit
                develop2_lines = [
                    "    │   ├── githash2/",
                    "    │   │   └── module1/",
                    "    │   │       └── index.html"
                ]
                develop2_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in develop2_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Update HEAD file position
                updated_head_lines = [
                    "    │   └── HEAD"  # HEAD now points to latest commit
                ]
                updated_head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in updated_head_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the new directory structure
                develop2_block.next_to(last_develop_block, DOWN, buff=block_spacing)
                develop2_block.align_to(last_develop_block, LEFT)

                # Calculate HEAD's new position
                updated_head_block.next_to(develop2_block, DOWN, buff=block_spacing)
                updated_head_block.align_to(develop2_block, LEFT)

                # Animate HEAD moving to new position (after the new commit)
                self.play(
                    current_block.animate.move_to(updated_head_block.get_center()),
                    run_time=0.4
                )

                # Show the new commit directory
                self.play(FadeIn(develop2_block), run_time=0.4)

                # Highlight the new commit directory
                glow_develop2 = develop2_block.copy()
                glow_develop2.set_color(BLUE)
                glow_develop2.set_stroke(width=4)

                # Animate the commit highlight
                self.play(
                    FadeIn(glow_develop2, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )
                self.play(FadeOut(glow_develop2), run_time=0.3)

                # Highlight HEAD being updated to point to new commit
                glow_head = current_block.copy()
                glow_head.set_color(BLUE)
                glow_head.set_stroke(width=4)

                # Animate the HEAD highlight
                self.play(
                    FadeIn(glow_head, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )
                self.play(FadeOut(glow_head), run_time=0.3)

                # Update reference to latest develop block
                last_develop_block = develop2_block

            elif i == 2:  # First pull request commit
                # Create directory structure for pull request
                pull_block_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       └── githash3/",
                    "    │           └── module1/",
                    "    │               └── index.html"
                ]
                pull_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in pull_block_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the pull request directory
                pull_block.next_to(current_block, DOWN, buff=block_spacing)
                pull_block.align_to(p_position, LEFT)

                # Show the pull request directory
                self.play(FadeIn(pull_block), run_time=0.4)

                # Highlight the new pull request directory
                glow_pull = pull_block.copy()
                glow_pull.set_color(ORANGE)
                glow_pull.set_stroke(width=4)

                # Animate the highlight
                self.play(
                    FadeIn(glow_pull, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )

                # Update directory structure to prepare for future commits
                pull_block_updated_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       ├── githash3/",  # Changed from └── to ├──
                    "    │       │   └── module1/",
                    "    │       │       └── index.html"
                ]
                pull_block_updated = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in pull_block_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Maintain correct positioning
                pull_block_updated.move_to(pull_block.get_center())
                pull_block_updated.align_to(pull_block, LEFT)

                # Add HEAD file for pull request branch
                head_file_lines = [
                    "    │       └── HEAD"  # HEAD file for pull request
                ]
                pull_head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")
                    for line in head_file_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the HEAD file
                pull_head_block.next_to(pull_block_updated, DOWN, buff=block_spacing)
                pull_head_block.align_to(pull_block_updated, LEFT)

                # Update directory structure and add HEAD file
                self.play(
                    FadeOut(glow_pull, run_time=0.25),
                    Transform(pull_block, pull_block_updated, run_time=0.3)
                )

                # Show the HEAD file appearing
                self.add(pull_head_block.set_opacity(0))
                head_fade_in = pull_head_block.animate.set_opacity(1)
                self.play(head_fade_in, run_time=0.2)

                # Highlight the HEAD file
                glow_head = pull_head_block.copy()
                glow_head.set_color(ORANGE)
                glow_head.set_stroke(width=4)
                glow_head.set_opacity(0)
                self.add(glow_head)

                # Animate the HEAD highlight
                glow_fade_in = glow_head.animate.set_opacity(1)
                self.play(glow_fade_in, run_time=0.3)
                glow_pulse = glow_head.animate.set_opacity(0.8)
                self.play(glow_pulse, run_time=0.2)
                self.play(FadeOut(glow_head), run_time=0.3)

                current_block = pull_head_block

            # Pause briefly between commits
            self.wait(0.3)

        # Create a tag for the second develop commit
        # Calculate tag position from commit coordinates
        tag_branch, tag_index = tag_commit
        tag_x = start_x + 0.85 + tag_index * x_step
        tag_y = y_develop if tag_branch == "develop" else y_pull

        # Define tag line (pointing up from commit)
        tag_line_start = [tag_x, tag_y, 0]
        tag_line_end = [tag_x, tag_y + 0.4, 0]
        square_position = tag_line_end

        # Create tag label
        tag_text = Text("v1.0.0", font_size=18, color=GREEN)
        tag_text.next_to(square_position, UP, buff=0.225)

        # Find the commit dot to place the tag line behind it
        commit_dot = None
        for dot in dots:
            if np.isclose(dot.get_center()[0], tag_x) and np.isclose(dot.get_center()[1], tag_y):
                commit_dot = dot
                break

        # Create invisible tag line (will be animated growing)
        tag_line = Line(tag_line_start, tag_line_start, color=GREEN)

        # Ensure tag line appears behind the commit dot
        if commit_dot:
            self.remove(commit_dot)
            self.add(tag_line)
            self.add(commit_dot)
        else:
            self.add(tag_line)

        # Animate tag line growing upward
        grow_line = tag_line.animate.put_start_and_end_on(tag_line_start, tag_line_end)
        self.play(grow_line, run_time=0.3)

        # Create tag marker (filled square)
        tag_square = Square(side_length=dot_radius*1.5, color=GREEN, fill_color=GREEN, fill_opacity=1).move_to(square_position)

        # Show tag marker and label
        self.play(
            FadeIn(tag_square),
            FadeIn(tag_text),
            run_time=0.4
        )

        # Add tags directory to file system tree
        tags_block_lines = [
            "    ├── tags/",
            "    │   └── v1.0.0/",  # The tag itself
            "    │       └── module1/",  # Direct path to content
            "    │           └── index.html"
        ]

        tags_block = VGroup(*[
            Text(line, font="Courier", font_size=16, color="#93a1a1")
            for line in tags_block_lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

        # Position tags directory in tree
        tags_block.next_to(current_block, DOWN, buff=block_spacing)
        tags_block.align_to(p_position, LEFT)

        # Update pull directory symbol (├── to └──) since tags will be last
        pull_first_line_replacement = Text("    └── pull/", font="Courier", font_size=18, color="#93a1a1")

        # Find first line of pull block
        if isinstance(pull_block, VGroup) and len(pull_block) > 0:
            pull_first_line = pull_block[0]
            pull_first_line_replacement.move_to(pull_first_line.get_center())
            pull_first_line_replacement.align_to(pull_first_line, LEFT)

        # Show tags directory
        self.play(FadeIn(tags_block), run_time=0.6)

        # Update pull directory symbol
        if 'pull_first_line' in locals() and 'pull_first_line_replacement' in locals():
            self.play(
                Transform(pull_first_line, pull_first_line_replacement),
                run_time=0.3
            )

        # Highlight tags directory
        glow_tags = tags_block.copy()
        glow_tags.set_color(GREEN)
        glow_tags.set_stroke(width=4)

        # Animate tags highlight
        self.play(
            FadeIn(glow_tags, rate_func=lambda t: np.sin(t * np.pi)),
            run_time=0.8
        )
        self.play(FadeOut(glow_tags), run_time=0.4)

        # Final pause to view completed visualization
        self.wait(2)