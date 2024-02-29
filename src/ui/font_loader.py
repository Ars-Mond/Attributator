import os
import sys
import dearpygui.dearpygui as imgui

MAIN_FONT: int | str = ''
HEADLINE_FONT: int | str = ''

# Capital "А" in Cyrillic.
big_let_start = 0x00C0

# Capital "Я" in Cyrillic.
big_let_end = 0x00DF

# Little "я" in Cyrillic
small_let_end = 0x00FF

# Initial number for the reassigned Cyrillic alphabet
remap_big_let = 0x0410

# adds a shift from large letters to small ones
alph_len = big_let_end - big_let_start + 1

# adds a transition from reassignment to non-reassignment
alph_shift = remap_big_let - big_let_start

def load(font_path: str):
    with imgui.font_registry():
        headline_font = imgui.add_font("./Resources/Font/JetBrainsMono-Bold.ttf", 32)

        with imgui.font(os.path.join(font_path, 'JetBrainsMono-Medium.ttf'), 18) as main_font:
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Default)
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Cyrillic)

            imgui.add_font_range(0x0391, 0x03C9)  # Greek character range
            imgui.add_font_range(0x2070, 0x209F)  # Range of upper and lower numerical indices

            # Fixing keyboard input on Windows
            if sys.platform == 'win32':
                _remap_chars()

    return main_font, headline_font


def _remap_chars():
    # Initial number for the reassigned Cyrillic alphabet
    biglet = remap_big_let

    # Cyclic switching of large letters
    for i1 in range(big_let_start, big_let_end + 1):
        # Reassigning the big letter
        imgui.add_char_remap(i1, biglet)

        # Reassign a small letter
        imgui.add_char_remap(i1 + alph_len, biglet + alph_len)

        # choose the next letter
        biglet += 1

    # The letters "Ёё" must be added separately, since they are located elsewhere in the table
    imgui.add_char_remap(0x00A8, 0x0401)
    imgui.add_char_remap(0x00B8, 0x0451)




# Parameters for Cyrillic conversion

# os.path.join(font_path, 'JetBrainsMono-Medium.ttf')
# main = imgui.add_font("./Resources/Font/Poppins-Medium.ttf", 18)
# footnote = imgui.add_font("./Resources/Font/Poppins-Medium.ttf", 14)