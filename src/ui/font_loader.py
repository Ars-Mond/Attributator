import os
import dearpygui.dearpygui as imgui


MAIN_FONT: int | str = ''
HEADLINE_FONT: int | str = ''

def load(font_path: str):
    # add a font registry
    with imgui.font_registry():

        with imgui.font(os.path.join(font_path, 'Poppins-Medium.ttf'), 18) as main_font:
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Default)
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Cyrillic)

        headline_font = imgui.add_font("./Resources/Font/Poppins-Bold.ttf", 32)

        # os.path.join(font_path, 'JetBrainsMono-Medium.ttf')
        # main = imgui.add_font("./Resources/Font/Poppins-Medium.ttf", 18)
        # footnote = imgui.add_font("./Resources/Font/Poppins-Medium.ttf", 14)

    global MAIN_FONT
    MAIN_FONT = main_font

    global HEADLINE_FONT
    HEADLINE_FONT = HEADLINE_FONT

    return main_font, headline_font

def get_headline():
    return HEADLINE_FONT