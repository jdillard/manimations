from manim import *
import random

class DocumentationHolarchy(Scene):
    def construct(self):
        # Set the background color to Solarized Dark theme
        self.camera.background_color = "#002b36"

        # Define how many times to show "word"
        num_words = 4

        # Step 1: Show letters spelling w, o, r, d
        # Position them in a row with spacing
        letter_objects = []
        spacing = 1.8
        total_width = (num_words - 1) * spacing
        start_x = -total_width / 2

        # Spell out "word" with one letter from each position
        word_letters = ["w", "o", "r", "d"]
        word_font_size = 24  # Smaller font size for words to show hierarchy

        for i in range(num_words):
            first_letter = Text(word_letters[i], font_size=word_font_size, color=BLUE)
            x_pos = start_x + i * spacing
            first_letter.move_to([x_pos, -1, 0])
            letter_objects.append(first_letter)

        # Show all the first letters appearing
        self.play(*[FadeIn(letter) for letter in letter_objects])
        self.wait(0.8)

        # Step 2: Fade in the remaining letters to complete each word
        word_objects = []
        fade_in_animations = []

        for i in range(num_words):
            # Create the complete word "word" - smaller size to show it's a lower level
            complete_word = Text("word", font_size=word_font_size, color=BLUE)
            x_pos = start_x + i * spacing
            complete_word.move_to([x_pos, -1, 0])
            word_objects.append(complete_word)

            # Transform the first letter into the complete word
            fade_in_animations.append(
                ReplacementTransform(letter_objects[i], complete_word)
            )

        self.play(*fade_in_animations)
        self.wait(1)

        # Step 3: Create the sentence above
        sentence = Text("sentence", font_size=36, color=ORANGE)
        sentence.move_to([0, 1, 0])

        # Show the sentence appearing
        self.play(FadeIn(sentence))
        self.wait(0.5)

        # Step 4: Create org-chart style angular lines going UPWARDS from words to sentence
        # Horizontal line that spans all words (positioned above the words)
        horizontal_y = 0.05  # Y position of the horizontal connecting line (above words)

        # Vertical lines from each word UP to horizontal line
        vertical_lines = []
        for word_obj in word_objects:
            line = Line(
                word_obj.get_top(),
                [word_obj.get_center()[0], horizontal_y, 0],
                color="#93a1a1",
                stroke_width=2
            )
            vertical_lines.append(line)

        # Horizontal line spanning across all word positions
        # Split into two halves that will meet in the middle
        left_x = start_x
        right_x = start_x + (num_words - 1) * spacing
        center_x = 0

        # Left half: from left edge to center
        horizontal_line_left = Line(
            [left_x, horizontal_y, 0],
            [center_x, horizontal_y, 0],
            color="#93a1a1",
            stroke_width=2
        )

        # Right half: from right edge to center
        horizontal_line_right = Line(
            [right_x, horizontal_y, 0],
            [center_x, horizontal_y, 0],
            color="#93a1a1",
            stroke_width=2
        )

        # Vertical line from horizontal line UP to sentence
        vertical_line = Line(
            [0, horizontal_y, 0],
            sentence.get_bottom(),
            color="#93a1a1",
            stroke_width=2
        )

        # Animate all the org-chart lines appearing (from bottom to top)
        self.play(*[Create(line) for line in vertical_lines])
        # Animate both halves of horizontal line meeting in the middle
        self.play(Create(horizontal_line_left), Create(horizontal_line_right))
        self.play(Create(vertical_line))
        self.wait(2)

        # ===== ZOOM OUT TO REVEAL BIGGER PICTURE =====
        # Group everything together for the zoom out
        level1_group = VGroup(
            *word_objects,
            *vertical_lines,
            horizontal_line_left,
            horizontal_line_right,
            vertical_line,
            sentence
        )

        # Step 5: Zoom out and reveal that "sentence" is part of a larger structure
        # After zoom, sentence should be same size as the original words (font 24)
        # Calculate scale factor: we want font 36 to become font 24
        target_size = word_font_size  # Should match original word size (24)
        original_sentence_size = 36
        scale_factor = target_size / original_sentence_size  # 24/36 = 0.667

        # First, create additional sentences that will be revealed
        num_sentences = 4
        sentence_objects = []

        # The current sentence will be one of them (we'll position it)
        # Create the other sentences - they should match the scaled-down size
        for i in range(num_sentences):
            if i == 1:  # This will be our existing sentence
                new_sentence = sentence
            else:
                # Create sentences at word_font_size to match scaled sentence
                new_sentence = Text("sentence", font_size=word_font_size, color=ORANGE)

            sentence_objects.append(new_sentence)

        # Position the new sentences to match the original word spacing
        # After zoom, they should be positioned like the words were originally
        for i in range(num_sentences):
            if i != 1:  # Don't move the existing sentence yet
                # Use the same spacing and positioning as original words
                x_pos = start_x + i * spacing
                y_pos = -1  # Same Y position as original words
                sentence_objects[i].move_to([x_pos, y_pos, 0])

        # Create the paragraph above - same size as original sentence (36)
        paragraph = Text("paragraph", font_size=36, color=GREEN)
        paragraph.move_to([0, 1, 0])

        # Create org-chart lines from sentences to paragraph
        # Lines should use same pattern as before - matching original word positions
        horizontal_y_2 = 0.05

        vertical_lines_2 = []
        for i in range(num_sentences):
            x_pos = start_x + i * spacing  # Same positions as original words
            line = Line(
                [x_pos, -1 + 0.2, 0],  # Top of sentence at word position
                [x_pos, horizontal_y_2, 0],
                color="#93a1a1",
                stroke_width=2
            )
            vertical_lines_2.append(line)

        # Horizontal line spanning same width as original
        horizontal_line_left_2 = Line(
            [left_x, horizontal_y_2, 0],
            [0, horizontal_y_2, 0],
            color="#93a1a1",
            stroke_width=2
        )

        horizontal_line_right_2 = Line(
            [right_x, horizontal_y_2, 0],
            [0, horizontal_y_2, 0],
            color="#93a1a1",
            stroke_width=2
        )

        vertical_line_2 = Line(
            [0, horizontal_y_2, 0],
            [0, 1 - 0.3, 0],  # Bottom of paragraph (at y=1)
            color="#93a1a1",
            stroke_width=2
        )

        # Animate the zoom out - scale everything down
        # This reveals the bigger picture
        # Need to position the sentence at index 1 position (start_x + 1*spacing, -1)
        # Current sentence is at (0, 1)
        # After scaling by 0.667, it will be at (0, 1.5 * 0.667) = (0, 1.0)
        # We want it at (start_x + spacing, -1)
        target_x = start_x + 1 * spacing  # Second position (index 1)
        target_y = -1

        # Calculate shift needed
        # Current position after scale: (0 * scale_factor, 1 * scale_factor)
        # Desired position: (target_x, target_y)
        shift_x = target_x - (0 * scale_factor)
        shift_y = target_y - (1 * scale_factor)

        self.play(
            level1_group.animate.scale(scale_factor).shift(RIGHT * shift_x + DOWN * (-shift_y)),
            run_time=2
        )
        self.wait(0.5)

        # Fade in the additional sentences, paragraph, and new connections
        self.play(
            *[FadeIn(sentence_objects[i]) for i in range(num_sentences) if i != 1],
            FadeIn(paragraph)
        )
        self.wait(0.5)

        # Draw the new org-chart connections
        self.play(*[Create(line) for line in vertical_lines_2])
        self.play(Create(horizontal_line_left_2), Create(horizontal_line_right_2))
        self.play(Create(vertical_line_2))
        self.wait(2)

        # ===== THIRD LEVEL: PARAGRAPH -> SECTION =====
        # Group level 2 for zoom out - include level1 so it moves with us
        level2_group = VGroup(
            level1_group,  # Include the previous level
            *sentence_objects,
            *vertical_lines_2,
            horizontal_line_left_2,
            horizontal_line_right_2,
            vertical_line_2,
            paragraph
        )

        # Create additional paragraphs
        num_paragraphs = 4
        paragraph_objects = []

        for i in range(num_paragraphs):
            if i == 2:  # This will be our existing paragraph (index 2, third position - shift right)
                new_paragraph = paragraph
            else:
                # Create paragraphs at word_font_size to match scaled paragraph
                new_paragraph = Text("paragraph", font_size=word_font_size, color=GREEN)

            paragraph_objects.append(new_paragraph)

        # Position the new paragraphs to match the original word spacing
        for i in range(num_paragraphs):
            if i != 2:  # Don't move the existing paragraph yet
                x_pos = start_x + i * spacing
                y_pos = -1  # Same Y position as original words
                paragraph_objects[i].move_to([x_pos, y_pos, 0])

        # Create the section above - same size as original sentence/paragraph (36)
        section = Text("section", font_size=36, color=ORANGE)
        section.move_to([0, 1, 0])

        # Create org-chart lines from paragraphs to section
        horizontal_y_3 = 0.05

        vertical_lines_3 = []
        for i in range(num_paragraphs):
            x_pos = start_x + i * spacing
            line = Line(
                [x_pos, -1 + 0.2, 0],
                [x_pos, horizontal_y_3, 0],
                color="#93a1a1",
                stroke_width=2
            )
            vertical_lines_3.append(line)

        horizontal_line_left_3 = Line(
            [left_x, horizontal_y_3, 0],
            [0, horizontal_y_3, 0],
            color="#93a1a1",
            stroke_width=2
        )

        horizontal_line_right_3 = Line(
            [right_x, horizontal_y_3, 0],
            [0, horizontal_y_3, 0],
            color="#93a1a1",
            stroke_width=2
        )

        vertical_line_3 = Line(
            [0, horizontal_y_3, 0],
            [0, 1 - 0.3, 0],
            color="#93a1a1",
            stroke_width=2
        )

        # Calculate shift for paragraph to align with other paragraphs
        # Position at index 2 (third position) to shift right
        target_x_para = start_x + 2 * spacing
        target_y_para = -1

        shift_x_para = target_x_para - (0 * scale_factor)
        shift_y_para = target_y_para - (1 * scale_factor)

        # Animate the zoom out
        self.play(
            level2_group.animate.scale(scale_factor).shift(RIGHT * shift_x_para + DOWN * (-shift_y_para)),
            run_time=2
        )
        self.wait(0.5)

        # Fade in the additional paragraphs, section, and new connections
        self.play(
            *[FadeIn(paragraph_objects[i]) for i in range(num_paragraphs) if i != 2],
            FadeIn(section)
        )
        self.wait(0.5)

        # Draw the new org-chart connections
        self.play(*[Create(line) for line in vertical_lines_3])
        self.play(Create(horizontal_line_left_3), Create(horizontal_line_right_3))
        self.play(Create(vertical_line_3))
        self.wait(2)

        # ===== FOURTH LEVEL: SECTION -> PAGE =====
        # Group level 3 for zoom out - include level2 so everything moves with us
        level3_group = VGroup(
            level2_group,  # Include the previous levels
            *paragraph_objects,
            *vertical_lines_3,
            horizontal_line_left_3,
            horizontal_line_right_3,
            vertical_line_3,
            section
        )

        # Create additional sections
        num_sections = 4
        section_objects = []

        for i in range(num_sections):
            if i == 0:  # This will be our existing section (index 0, first position - shift left)
                new_section = section
            else:
                # Create sections at word_font_size to match scaled section
                new_section = Text("section", font_size=word_font_size, color=ORANGE)

            section_objects.append(new_section)

        # Position the new sections to match the original word spacing
        for i in range(num_sections):
            if i != 0:  # Don't move the existing section yet
                x_pos = start_x + i * spacing
                y_pos = -1  # Same Y position as original words
                section_objects[i].move_to([x_pos, y_pos, 0])

        # Create the page above - same size as original sentence/paragraph/section (36)
        page = Text("page", font_size=36, color=BLUE)
        page.move_to([0, 1, 0])

        # Create org-chart lines from sections to page
        horizontal_y_4 = 0.05

        vertical_lines_4 = []
        for i in range(num_sections):
            x_pos = start_x + i * spacing
            line = Line(
                [x_pos, -1 + 0.2, 0],
                [x_pos, horizontal_y_4, 0],
                color="#93a1a1",
                stroke_width=2
            )
            vertical_lines_4.append(line)

        horizontal_line_left_4 = Line(
            [left_x, horizontal_y_4, 0],
            [0, horizontal_y_4, 0],
            color="#93a1a1",
            stroke_width=2
        )

        horizontal_line_right_4 = Line(
            [right_x, horizontal_y_4, 0],
            [0, horizontal_y_4, 0],
            color="#93a1a1",
            stroke_width=2
        )

        vertical_line_4 = Line(
            [0, horizontal_y_4, 0],
            [0, 1 - 0.3, 0],
            color="#93a1a1",
            stroke_width=2
        )

        # Calculate shift for section to align with other sections
        # Position at index 0 (first position) to shift left
        target_x_section = start_x + 0 * spacing
        target_y_section = -1

        shift_x_section = target_x_section - (0 * scale_factor)
        shift_y_section = target_y_section - (1 * scale_factor)

        # Animate the zoom out
        self.play(
            level3_group.animate.scale(scale_factor).shift(RIGHT * shift_x_section + DOWN * (-shift_y_section)),
            run_time=2
        )
        self.wait(0.5)

        # Fade in the additional sections, page, and new connections
        self.play(
            *[FadeIn(section_objects[i]) for i in range(num_sections) if i != 0],
            FadeIn(page)
        )
        self.wait(0.5)

        # Draw the new org-chart connections
        self.play(*[Create(line) for line in vertical_lines_4])
        self.play(Create(horizontal_line_left_4), Create(horizontal_line_right_4))
        self.play(Create(vertical_line_4))
        self.wait(3)
