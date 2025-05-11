from manim import *


class GitAndTreeSplit(Scene):
    def construct(self):
        self.camera.background_color = "#002b36"

        # Create the Git flow diagram on the left side
        git_group = VGroup()

        # Define start points for branches
        start_x = -5
        x_step = 1.2

        # Branch Y positions
        y_develop = 1
        y_pull = 0

        # Branch labels
        labels = [
            ("develop", y_develop, BLUE),
            ("pull/1234", y_pull, ORANGE)
        ]

        # Create labels
        branch_labels = VGroup()
        for name, y, color in labels:
            label = Text(name, font_size=24, color=color).next_to([start_x, y, 0], LEFT + RIGHT * 1.0)
            self.play(Write(label), run_time=0.3)
            branch_labels.add(label)
            git_group.add(label)

        # Initialize paths
        lines = {
            "develop": Line([start_x + 0.85, y_develop, 0], [start_x + 0.85, y_develop, 0], color=BLUE),
            "pull": Line([start_x + 0.85, y_pull, 0], [start_x + 0.85, y_pull, 0], color=ORANGE),
        }

        # Show line starting points
        for line in lines.values():
            self.play(Create(line), run_time=0.2)
            git_group.add(line)

        # Define commits
        commits = [
            ("develop", 1),
            ("develop", 2),
            ("pull", 1),
        ]

        # Define which commit to tag (later)
        tag_commit = ("develop", 2)  # Tag the second develop commit as v1.0.0

        dot_radius = 0.12
        dots = VGroup()

        # Now create tree side - shifted UP for better vertical centering
        tree_origin = RIGHT * 2.5 + UP * 3.5  # Moved UP slightly (from UP * 3 to UP * 3.5)
        line_spacing = 0.15  # Reduced spacing between lines
        block_spacing = 0.08  # Reduced spacing between blocks

        # Starting point with smaller font size
        tree_lines = [
            ".",
            "└── packages/"
        ]

        # Create the initial tree structure with smaller font size
        text_objs = [Text(line, font="Courier", font_size=18, color="#93a1a1") for line in tree_lines]  # Reduced from 20 to 18
        tree_group = VGroup(*text_objs).arrange(DOWN, aligned_edge=LEFT)

        # Position the tree group at the tree_origin
        tree_group.move_to(tree_origin, aligned_edge=UP+RIGHT)

        self.play(*[Write(line) for line in tree_group])
        self.wait(0.5)

        # Calculate the position of the 'p' in 'packages/' to use for indentation reference
        root_line = text_objs[1]  # This is "└── packages/"

        # Find the position of the 'p' in "packages/"
        # The characters are "└── p" so we need the 5th character
        p_index = 4  # Zero-based indexing (└, ─, ─, <space>, p)
        p_position = root_line.get_left() + RIGHT * p_index * root_line.width / len("└── packages/")

        # Process commits and tree growth together
        current_block = tree_group
        head_block = None  # Reference to track the HEAD block

        # We'll keep track of the last commit block for each branch
        last_develop_block = None

        for i, (branch, index) in enumerate(commits):
            # Git side: Extend branch line
            x = start_x + 0.85 + index * x_step
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
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in develop1_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the block with proper indentation
                # Align the left edge of this block with the p_position
                develop1_block.next_to(current_block, DOWN, buff=block_spacing)
                develop1_block.align_to(p_position, LEFT)

                self.play(FadeIn(develop1_block), run_time=0.4)
                last_develop_block = develop1_block

                # Add glow effect for develop/githash1 (blue)
                glow_develop1 = develop1_block.copy()
                glow_develop1.set_color(BLUE)
                glow_develop1.set_stroke(width=4)

                # Apply glow animation
                self.play(
                    FadeIn(glow_develop1, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )

                # Prepare updated develop block structure to change └── to ├── for githash1
                develop1_updated_lines = [
                    "    ├── develop/",
                    "    │   ├── githash1/",  # Changed from └── to ├──
                    "    │   │   └── my-package/",
                    "    │   │       └── index.html"
                ]
                develop1_updated = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in develop1_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Ensure the updated block maintains the same position
                develop1_updated.move_to(develop1_block.get_center())
                develop1_updated.align_to(develop1_block, LEFT)

                # Prepare HEAD file content
                develop_head_lines = [
                    "    │   └── HEAD"  # HEAD file as sibling to githash1
                ]
                head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in develop_head_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                head_block.next_to(develop1_updated, DOWN, aligned_edge=LEFT, buff=block_spacing)
                # Align HEAD with the same indentation as the develop1_updated block
                head_block.align_to(develop1_updated, LEFT)

                # Start fading out the develop glow WHILE updating structure
                self.play(
                    FadeOut(glow_develop1, run_time=0.25),
                    Transform(develop1_block, develop1_updated, run_time=0.3)
                )

                # Fade in the HEAD file
                self.add(head_block.set_opacity(0))
                head_fade_in = head_block.animate.set_opacity(1)
                self.play(head_fade_in, run_time=0.2)

                # Start the HEAD glow effect
                glow_develop_head = head_block.copy()
                glow_develop_head.set_color(BLUE)
                glow_develop_head.set_stroke(width=4)
                glow_develop_head.set_opacity(0)
                self.add(glow_develop_head)

                # Fade in and animate the glow
                glow_fade_in = glow_develop_head.animate.set_opacity(1)
                self.play(glow_fade_in, run_time=0.3)
                glow_pulse = glow_develop_head.animate.set_opacity(0.8)
                self.play(glow_pulse, run_time=0.2)
                self.play(FadeOut(glow_develop_head), run_time=0.3)

                current_block = head_block
                last_develop_block = develop1_block  # Keep track of last develop block

            elif i == 1:  # Second develop commit
                # First, we need to update the structure to show ├── for githash1
                # We'll shift the HEAD file down to make room for githash2

                # Prepare the githash2 block
                develop2_lines = [
                    "    │   ├── githash2/",  # Using ├── instead of └── since HEAD will come after
                    "    │   │   └── my-package/",
                    "    │   │       └── index.html"
                ]
                develop2_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in develop2_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Update HEAD line to show as └── since it will be the last item
                updated_head_lines = [
                    "    │   └── HEAD"  # HEAD remains the last item with └──
                ]
                updated_head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in updated_head_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position develop2_block where it needs to go (after githash1)
                develop2_block.next_to(last_develop_block, DOWN, buff=block_spacing)
                # Maintain the same alignment as last_develop_block
                develop2_block.align_to(last_develop_block, LEFT)

                # Calculate where HEAD should end up
                updated_head_block.next_to(develop2_block, DOWN, buff=block_spacing)
                updated_head_block.align_to(develop2_block, LEFT)

                # Animate HEAD sliding down to make room for githash2
                self.play(
                    current_block.animate.move_to(updated_head_block.get_center()),
                    run_time=0.4
                )

                # Now fade in githash2
                self.play(FadeIn(develop2_block), run_time=0.4)

                # Glow effect for githash2
                glow_develop2 = develop2_block.copy()
                glow_develop2.set_color(BLUE)
                glow_develop2.set_stroke(width=4)

                # Apply glow animation to githash2
                self.play(
                    FadeIn(glow_develop2, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )
                self.play(FadeOut(glow_develop2), run_time=0.3)

                # Now glow the HEAD file to show it's being updated
                glow_head = current_block.copy()
                glow_head.set_color(BLUE)
                glow_head.set_stroke(width=4)

                # Apply glow animation for HEAD update
                self.play(
                    FadeIn(glow_head, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )
                self.play(FadeOut(glow_head), run_time=0.3)

                # Keep track of the new commit block
                last_develop_block = develop2_block

            elif i == 2:  # First pull request commit
                pull_block_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       └── githash3/",
                    "    │           └── my-package/",
                    "    │               └── index.html"
                ]
                pull_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in pull_block_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Position the pull block with proper indentation
                pull_block.next_to(current_block, DOWN, buff=block_spacing)
                # Align with the p_position to maintain consistent indentation
                pull_block.align_to(p_position, LEFT)

                self.play(FadeIn(pull_block), run_time=0.4)

                # Add glow effect for pull/1234 (orange)
                glow_pull = pull_block.copy()
                glow_pull.set_color(ORANGE)
                glow_pull.set_stroke(width=4)

                # Start the pull/1234 glow animation
                self.play(
                    FadeIn(glow_pull, rate_func=lambda t: np.sin(t * np.pi)),
                    run_time=0.6
                )

                # Prepare updated pull block structure
                pull_block_updated_lines = [
                    "    ├── pull/",
                    "    │   └── 1234/",
                    "    │       ├── githash3/",  # Changed from └── to ├──
                    "    │       │   └── my-package/",
                    "    │       │       └── index.html"
                ]
                pull_block_updated = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in pull_block_updated_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                # Maintain position and alignment of the updated block
                pull_block_updated.move_to(pull_block.get_center())
                pull_block_updated.align_to(pull_block, LEFT)

                # Prepare HEAD file content for pull branch
                head_file_lines = [
                    "    │       └── HEAD"  # HEAD file as sibling to githash3
                ]
                pull_head_block = VGroup(*[
                    Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
                    for line in head_file_lines
                ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

                pull_head_block.next_to(pull_block_updated, DOWN, buff=block_spacing)
                pull_head_block.align_to(pull_block_updated, LEFT)

                # Start fading out the pull glow WHILE updating structure
                self.play(
                    FadeOut(glow_pull, run_time=0.25),
                    Transform(pull_block, pull_block_updated, run_time=0.3)
                )

                # Fade in the HEAD file
                self.add(pull_head_block.set_opacity(0))
                head_fade_in = pull_head_block.animate.set_opacity(1)
                self.play(head_fade_in, run_time=0.2)

                # Start the HEAD glow effect
                glow_head = pull_head_block.copy()
                glow_head.set_color(ORANGE)
                glow_head.set_stroke(width=4)
                glow_head.set_opacity(0)
                self.add(glow_head)

                # Fade in and animate the glow
                glow_fade_in = glow_head.animate.set_opacity(1)
                self.play(glow_fade_in, run_time=0.3)
                glow_pulse = glow_head.animate.set_opacity(0.8)
                self.play(glow_pulse, run_time=0.2)
                self.play(FadeOut(glow_head), run_time=0.3)

                current_block = pull_head_block

            # Let each step be visible
            self.wait(0.3)

        # Calculate the position of the tag commit dot
        tag_branch, tag_index = tag_commit
        tag_x = start_x + 0.85 + tag_index * x_step
        tag_y = y_develop if tag_branch == "develop" else y_pull

        # Make the green line 2/3 as long as before (0.6 → 0.4)
        tag_line_start = [tag_x, tag_y, 0]
        tag_line_end = [tag_x, tag_y + 0.4, 0]  # Reduced from 0.6 to 0.4 (2/3 of previous length)

        # Define the square position at the end of the line
        square_position = tag_line_end

        # Create a tag label properly positioned above the square with more space for separation
        tag_text = Text("v1.0.0", font_size=18, color=GREEN)
        tag_text.next_to(square_position, UP, buff=0.225)  # Increased buffer by 1.5x (from 0.15 to 0.225)

        # Get the dot at the commit position to place the line behind it
        commit_dot = None
        for dot in dots:
            if np.isclose(dot.get_center()[0], tag_x) and np.isclose(dot.get_center()[1], tag_y):
                commit_dot = dot
                break

        # Create the line but make it invisible initially - PLACE IT BEHIND THE DOT
        tag_line = Line(tag_line_start, tag_line_start, color=GREEN)

        # If we found the commit dot, add the line BEHIND it
        if commit_dot:
            self.remove(commit_dot)
            self.add(tag_line)
            self.add(commit_dot)  # Re-add the dot to ensure it's in front
        else:
            self.add(tag_line)

        # Animate the line growing upward
        grow_line = tag_line.animate.put_start_and_end_on(tag_line_start, tag_line_end)
        self.play(grow_line, run_time=0.3)

        # Create a filled square instead of an empty one
        tag_square = Square(side_length=dot_radius*1.5, color=GREEN, fill_color=GREEN, fill_opacity=1).move_to(square_position)

        # Fade in the square and the text at the same time
        self.play(
            FadeIn(tag_square),
            FadeIn(tag_text),
            run_time=0.4
        )

        # Now update the directory tree to include the tags directory
        tags_block_lines = [
            "    ├── tags/",
            "    │   └── v1.0.0/",  # The tag itself
            "    │       └── my-package/",  # Directly to my-package (no githash2 directory)
            "    │           └── index.html"
        ]

        tags_block = VGroup(*[
            Text(line, font="Courier", font_size=16, color="#93a1a1")  # Reduced from 18 to 16
            for line in tags_block_lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=line_spacing)

        # Instead of trying to find the pull directory in existing tree,
        # let's position the tags directory based on what we know
        # Position it after current_block (the pull HEAD block)
        tags_block.next_to(current_block, DOWN, buff=block_spacing)
        tags_block.align_to(p_position, LEFT)

        # Create a replacement for the pull block first line (changing ├── to └──)
        # Since we know that the pull_block variable contains our pull directory block
        # We need a simpler approach that doesn't try to search through all mobjects
        pull_first_line_replacement = Text("    └── pull/", font="Courier", font_size=18, color="#93a1a1")

        # Find the first line of the existing pull block
        # Pull block is already tracked from commit 3
        if isinstance(pull_block, VGroup) and len(pull_block) > 0:
            # Get the first submobject (first line) of the pull block
            pull_first_line = pull_block[0]  # First item in the VGroup

            # Position the replacement text
            pull_first_line_replacement.move_to(pull_first_line.get_center())
            pull_first_line_replacement.align_to(pull_first_line, LEFT)

        # Create the animation for the tags directory
        self.play(FadeIn(tags_block), run_time=0.6)

        # If we found the pull first line, update it to be the last item (└── instead of ├──)
        if 'pull_first_line' in locals() and 'pull_first_line_replacement' in locals():
            self.play(
                Transform(pull_first_line, pull_first_line_replacement),
                run_time=0.3
            )

        # Add glow effect for the tags directory
        glow_tags = tags_block.copy()
        glow_tags.set_color(GREEN)
        glow_tags.set_stroke(width=4)

        # Apply glow animation
        self.play(
            FadeIn(glow_tags, rate_func=lambda t: np.sin(t * np.pi)),
            run_time=0.8
        )
        self.play(FadeOut(glow_tags), run_time=0.4)

        # Final pause to see the completed visualization
        self.wait(2)