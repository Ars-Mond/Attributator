import os
import sys

from loguru import logger

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

from src.config.config_provider import ConfigProvider
import src.ui.application as app
import src.ui.font_loader as fl


# ========= INIT_PATH ================================================
application_path = ''
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
else:
    application_path = os.path.abspath('./')

RESOURCE_PATH = os.path.join(application_path, 'resources')
DATA_PATH = os.path.join(application_path, 'data')

IMAGES_PATH = os.path.join(RESOURCE_PATH, 'images')
SAVE_FILE_PATH = os.path.abspath('./data/save.ini')


# ========= LOGGER ===================================================
logger_format = '[{time} | {level:10}]: {message}'

logger.add('./data/logs/debug.log', format=logger_format, rotation='1 MB', compression='zip')

# logger_format2 = '[<green>{time}</green> | {level:10}]: {message}'

# ========= CONFIG PROVIDER ==========================================
SETTINGS_CONFIG_PATH = RESOURCE_PATH
SETTINGS_CONFIG_NAME = 'settings'

TAGS_CONFIG_PATH = RESOURCE_PATH
TAGS_CONFIG_NAME = 'tags'

settings = ConfigProvider(path_file=SETTINGS_CONFIG_PATH, name_file=SETTINGS_CONFIG_NAME)
tags = ConfigProvider(path_file=TAGS_CONFIG_PATH, name_file=TAGS_CONFIG_NAME)


def save_init():
    imgui.save_init_file(SAVE_FILE_PATH)

if __name__ == '__main__':
    @logger.catch
    def _start():
        logger.info('Start App!')
        imgui.create_context()

        font_path = os.path.join(RESOURCE_PATH, 'font/')
        main_font, headline_font = fl.load(font_path)
        imgui.bind_font(main_font)

        windows = app.init_window(abs_data_path=DATA_PATH, headline_font=headline_font)

        # imgui.set_primary_window(app.primary_window(), True)

        # demo.show_demo()

        imgui.configure_app(docking=True, docking_space=True, init_file=SAVE_FILE_PATH)
        imgui.create_viewport(title='Attributator')

        imgui.set_viewport_small_icon(os.path.join(IMAGES_PATH, 'icon.ico'))
        imgui.set_viewport_large_icon(os.path.join(IMAGES_PATH, 'icon_x2.ico'))

        imgui.setup_dearpygui()

        imgui.set_exit_callback(callback=lambda: save_init())

        # imgui.show_viewport()
        # while imgui.is_dearpygui_running():
        #     imgui.render_dearpygui_frame()

        imgui.show_viewport()
        imgui.start_dearpygui()
        imgui.destroy_context()
        logger.info('Stop App!')

    _start()

