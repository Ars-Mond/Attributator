import os

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

from src.config.config_provider import ConfigProvider
import src.ui.application as app
import src.ui.font_loader as fl
import src.ui.theme as theme

init_file = os.path.abspath('./data/imgui.ini')
font_path = os.path.abspath('./resources/font/')

# ========== CONFIG PROVIDER ===========================================
SETTINGS_CONFIG_PATH = './resources'
SETTINGS_CONFIG_NAME = 'settings'

TAGS_CONFIG_PATH = './resources'
TAGS_CONFIG_NAME = 'tags'

settings = ConfigProvider(path_file=SETTINGS_CONFIG_PATH, name_file=SETTINGS_CONFIG_NAME)
tags = ConfigProvider(path_file=TAGS_CONFIG_PATH, name_file=TAGS_CONFIG_NAME)


def save_init():
    imgui.save_init_file(init_file)

if __name__ == '__main__':
    imgui.create_context()

    main_font, headline_font = fl.load(font_path)
    imgui.bind_font(main_font)

    windows = app.init_window(headline_font=headline_font)

    # imgui.set_primary_window(app.primary_window(), True)

    # demo.show_demo()

    # global_theme = theme.l()

    # imgui.bind_theme(global_theme)
    imgui.configure_app(docking=True, docking_space=True, init_file=init_file)
    imgui.create_viewport(title='Attributator') # clear_color=(255, 255, 255, 255)
    imgui.setup_dearpygui()

    imgui.set_exit_callback(callback=lambda: save_init())

    # imgui.show_viewport()
    # while imgui.is_dearpygui_running():
    #     imgui.render_dearpygui_frame()

    imgui.show_viewport()
    imgui.start_dearpygui()
    imgui.destroy_context()