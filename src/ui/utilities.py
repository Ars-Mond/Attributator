import dearpygui.dearpygui as imgui
def separate_spacer(*, heigth: int = 0):
    l = int(heigth / 2)
    imgui.add_spacer(height=l)
    imgui.add_separator()
    imgui.add_spacer(height=l)