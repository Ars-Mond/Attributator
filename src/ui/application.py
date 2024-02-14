import os
from typing import Callable, TypeVar

T = TypeVar('T')
ClassType = TypeVar('ClassType')

import xdialog
from loguru import logger

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

import src.core.control as ctrl
import src.ui.utilities as util
import src.ui.font_loader as fl

from src.core.deprecated import deprecated
from src.config.config_provider import ConfigProvider


# ========= DEFINE ===================================================
g = '#ff00ff'

file_types = ['jpg', 'png', 'mp4']

MAIN_WINDOW_ID = 'main-window'
ABOUT_ID = 'about-window'
PREVIEW_WINDOW_ID = 'preview-window'

FILE_LIST_ID = 'file-list'
class FIELD_ID:
    FILENAME = 'filename-id'
    TITLE = 'title-id'
    DESCRIPTION = 'description-id'
    CATEGORY = 'category-id'
    RELEASE = 'release-id'
    KEYWORDS = 'keywords-id'

    MATURE_CONTENT = 'mature-id'
    ILLUSTRATION = 'illustration-id'
    EDITORIAL = 'editorial-id'

    PRICE_1 = 'price-1-id'
    PRICE_2 = 'price-2-id'


# ========= FONT =====================================================
HEADLINE_FONT: int | str = ''


# ========= DATA =====================================================
currentDir = ''
currentFile = ''

configFiles: list[dict] = []


# ========= TEST =====================================================
OLD_INPUT_TEXT_VALUE = ''


# ========= WINDOWS ==================================================
def init_window(*, headline_font: int | str):
    global HEADLINE_FONT
    HEADLINE_FONT = headline_font

    mw = main_window()
    pw = preview_window()
    aw = about_window()

    logger.info('Inited windows')

    return [mw, aw, pw]

@logger.catch
def main_window():
    with imgui.window(label='Main', tag=MAIN_WINDOW_ID, show=True, no_close=True, no_collapse=True, min_size=[620, 480]) as window:
        with imgui.menu_bar():
            with imgui.menu(label="File"):
                imgui.add_menu_item(label='Open...')
                imgui.add_menu_item(label='Save')
                imgui.add_menu_item(label='Save as...')

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Open directory...', callback=_set_files_in_view)

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Export...')

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Settings')

            with imgui.menu(label='Window'):
                imgui.add_menu_item(label='Preview', callback=lambda: _show_window(PREVIEW_WINDOW_ID))
                imgui.add_menu_item(label='Tag Manager')
                imgui.add_menu_item(label='Demo', callback=demo.show_demo)
                imgui.add_menu_item(label='Dialog')

            with imgui.menu(label='Help'):
                imgui.add_menu_item(label='Docs', callback=lambda: xdialog.info('Звоните Сене!', 'Что то сломалось!? Звони Адмэну! тел: 8 800 333-35-35.'))
                imgui.add_menu_item(label='About...', callback=lambda: _show_window(ABOUT_ID))

        with imgui.table(header_row=False, borders_outerH=False, borders_outerV=False, resizable=True):
            imgui.add_table_column()
            imgui.add_table_column()
            with imgui.table_row():
                with imgui.table_cell():
                    imgui.add_text(default_value="List")
                    with imgui.child_window(height=-15, tag=FILE_LIST_ID):
                        # list files
                        pass

                    imgui.add_spacer(height=5)

                with imgui.table_cell():
                    imgui.add_text(default_value="Tools")
                    with imgui.child_window(height=-15):
                        imgui.add_input_text(label='Filename*', tag=FIELD_ID.FILENAME)
                        imgui.add_input_text(label='Title*', tag=FIELD_ID.TITLE)
                        imgui.add_input_text(label='Description*', tag=FIELD_ID.DESCRIPTION, multiline=True)
                        imgui.add_input_text(label='Categories', tag=FIELD_ID.CATEGORY)
                        imgui.add_input_text(label='Release Filename', tag=FIELD_ID.RELEASE)
                        imgui.add_input_text(label='Keywords*', tag=FIELD_ID.KEYWORDS, multiline=True, callback=wrap_input_text, on_enter=True)

                        imgui.add_spacer(height=1)

                        with imgui.tree_node(label='Advanced'):
                            with imgui.group(horizontal=True):
                                imgui.add_checkbox(label='Mature content')
                                imgui.add_checkbox(label='Illustration')
                                imgui.add_checkbox(label='Editorial')

                            imgui.add_spacer(height=2)

                            with imgui.group(horizontal=False):
                                imgui.add_input_float(label='Price*', tag=FIELD_ID.PRICE_1, width=100, step=1, step_fast=10, format='%.1f')
                                _help_last('Envato video price:\n' +
                                           'Price: Single Use License ($USD)')
                                imgui.add_input_float(label='Price 2*', tag=FIELD_ID.PRICE_2, width=100, step=1, step_fast=10, format='%.1f')
                                _help_last('Envato video price:\n' +
                                           'Price: Multi-use License ($USD)')

                        imgui.add_spacer(height=10)

                        imgui.add_separator()
                        imgui.add_spacer(height=10)

                        imgui.add_button(label="Set", width=-1, callback=_save_value)
                        imgui.add_button(label="Clear", width=-1)

                        imgui.add_spacer(height=20)

                        imgui.add_button(label="Save", width=-1)
                        # imgui.add_button(label="Remove", width=-1)

    return window

def preview_window():
    texture_data = []
    for i in range(0, 500):
        for j in range(0, 500):
            texture_data.append(i / 620)
            texture_data.append(i / 620)
            texture_data.append(i / 620)
            texture_data.append(1)

    with imgui.texture_registry(label='textures'):
        imgui.add_dynamic_texture(label='preview-texture', width=500, height=500, default_value=texture_data, tag="texture_tag")
        
    with imgui.window(label='Preview', tag=PREVIEW_WINDOW_ID, show=False) as window:
        imgui.add_image("texture_tag")

    return window

def about_window():
    with imgui.window(label='About', tag=ABOUT_ID, show=False, modal=True, no_title_bar=True) as window:
        hl = imgui.add_text(default_value='Priver PIDOR')
        imgui.bind_item_font(hl, HEADLINE_FONT)
        imgui.add_button(label='Close', callback=lambda: imgui.hide_item(ABOUT_ID))

    imgui.set_item_pos(window, [300, 300])

    return window

def _set_files_in_view():
    files, dir_path = ctrl.show_dialog(file_types)
    if files is not None:
        _render_file_view(files)

        global currentDir
        currentDir = dir_path

        f = ctrl.get_dir_config(dir_path)

        if f is None:
            return

        files_config = dict.get(f, 'files')
        if files_config is not None:
            global configFiles
            configFiles = files_config

def _save_value(sender, app_data, user_data):
    if not os.path.exists(currentFile):
        return

    filename = imgui.get_value(FIELD_ID.FILENAME)
    title = imgui.get_value(FIELD_ID.TITLE)
    description = imgui.get_value(FIELD_ID.DESCRIPTION)
    category = imgui.get_value(FIELD_ID.CATEGORY)
    release = imgui.get_value(FIELD_ID.RELEASE)
    keywords = imgui.get_value(FIELD_ID.KEYWORDS)

    if not is_valid(filename):
        logger.warning('The "filename" field is not filled in.')
        _show_error("Field error", 'The "filename" field is not filled in.')
        return
    if not is_valid(title):
        logger.warning('The "title" field is not filled in.')
        _show_error("Field error", 'The "title" field is not filled in.')
        return
    if not is_valid(description):
        logger.warning('The "description" field is not filled in.')
        _show_error("Field error", 'The "description" field is not filled in.')
        return
    if not is_valid(keywords):
        logger.warning('The "tags" field is not filled in.')
        _show_error("Field error", 'The "tags" field is not filled in.')
        return

    file = {
        'path': currentFile,
        'filename': filename,
        'title': title,
        'description': description,
        'category': category,
        'release_filename': release,
        'keywords': keywords,
        'mature_content': False,
        'illustration': False,
        'editorial': False,
        'price1': 0.0,
        'price2': 0.0,
    }

    print(file)

    # global configFiles
    configFiles.append(file)

    ctrl.set_dir_config(currentDir, {'files': configFiles})

def _render_file_view(files: list[str]):
    children = imgui.get_item_children(FILE_LIST_ID)

    for k, v in children.items():
        if v is not None:
            for i in v:
                imgui.delete_item(i)

    items = []

    for file in files:
        seletion = imgui.add_selectable(label=os.path.basename(file), parent=FILE_LIST_ID, callback=_select_file, user_data=[items, file])
        items.append(seletion)


def _select_file(sender, app_data, user_data):
    logger.debug(f'{sender} | {app_data} | {user_data}')
    def _selection(items):
        for item in items:
            if item != sender:
                imgui.set_value(item, False)

    _selection(user_data[0])

    global currentFile
    currentFile = user_data[1]

    file = select(configFiles, lambda item: item.get('path') == user_data[1])
    if file is not None:
        logger.info(f'File data found. {file.get('path')}')

        filename = str(file.get('filename'))
        title = str(file.get('title'))
        description = str(file.get('description'))
        category = str(file.get('category'))
        release = str(file.get('release_filename'))
        keywords = list(file.get('keywords'))

        mature_content = bool(file.get('mature_content'))
        illustration = bool(file.get('illustration'))
        editorial = bool(file.get('editorial'))
        price1 = float(file.get('price1'))
        price2 = float(file.get('price2'))

        imgui.set_value(FIELD_ID.FILENAME, filename)
        imgui.set_value(FIELD_ID.TITLE, title)
        imgui.set_value(FIELD_ID.DESCRIPTION, description)
        imgui.set_value(FIELD_ID.CATEGORY, category)
        imgui.set_value(FIELD_ID.RELEASE, release)
        imgui.set_value(FIELD_ID.KEYWORDS, keywords)

        imgui.set_value(FIELD_ID.MATURE_CONTENT, mature_content)
        imgui.set_value(FIELD_ID.ILLUSTRATION, illustration)
        imgui.set_value(FIELD_ID.EDITORIAL, editorial)
        imgui.set_value(FIELD_ID.PRICE_1, price1)
        imgui.set_value(FIELD_ID.PRICE_2, price2)
        return


    imgui.set_value(FIELD_ID.FILENAME, os.path.basename(user_data[1]))
    imgui.set_value(FIELD_ID.TITLE, '')
    imgui.set_value(FIELD_ID.DESCRIPTION, '')
    imgui.set_value(FIELD_ID.CATEGORY, '')
    imgui.set_value(FIELD_ID.RELEASE, '')
    imgui.set_value(FIELD_ID.KEYWORDS, '')


# ========= UTILITIES ================================================
def _show_window(tag: int | str):
    imgui.show_item(tag)

def _show_error(title: str, message: str):
    return xdialog.error(title, message)

def _help_last(message: str | list[str], join_str: str = '\n'):
    last_item = imgui.last_item()
    _help(last_item, message, join_str)

def _help(tag: int | str, message: str | list[str], join_str: str = '\n'):
    temp_message = message
    if isinstance(message, list):
        temp_message = join_str.join(message)

    group = imgui.add_group(horizontal=True)
    imgui.move_item(tag, parent=group)
    imgui.capture_next_item(lambda s: imgui.move_item(s, parent=group))
    t = imgui.add_text("(?)", color=[0, 255, 0])
    with imgui.tooltip(t):
        imgui.add_text(temp_message)

def wrap_input_text(sender, app_data: str, user_data):
    global OLD_INPUT_TEXT_VALUE

    if app_data == OLD_INPUT_TEXT_VALUE:
        return


    size_text_box = imgui.get_item_rect_size(sender)
    print(size_text_box)
    print(imgui.get_text_size(app_data, wrap_width=size_text_box[0]))
    print(app_data)
    print('==============')

    ts = app_data.replace('\n', '').split(',')

    ts_new = []

    max_str_count = int(size_text_box[0] / 5) - 10

    out = ''
    out_list = []

    for t in ts:
        if len(t) <= 0: continue

        r = t.strip(' ')
        ts_new.append(r)
        if len(out + r + ', ') <= max_str_count:
            out += r + ', '
        else:
            out_list.append(out)
            out = ''

    out_list.append(out)

    l = '\n'.join(out_list)
    imgui.set_value(sender, l)

    OLD_INPUT_TEXT_VALUE = l


# ========= DEPRECATED ===============================================
@deprecated
def primary_window():
    with imgui.window(no_close=True, menubar=True) as w:
        with imgui.menu_bar() as bar:
            with imgui.menu(label='Window'):
                imgui.add_menu_item(label='Geometry Editor')
                imgui.add_menu_item(label='Node Editor')

            with imgui.menu(label='Help'):
                imgui.add_menu_item(label='Help')
                imgui.add_menu_item(label='About')
                imgui.add_spacer(height=10)
                imgui.add_separator()
                imgui.add_menu_item(label='show_demo', callback=lambda: demo.show_demo())
                imgui.add_menu_item(label='show_style_editor', callback=lambda: imgui.show_style_editor())
                imgui.add_menu_item(label='show_font_manager', callback=lambda: imgui.show_font_manager())

    return w


# ========= OTHER ====================================================
def is_valid(value: str) -> bool:
    return value is not None and len(value) > 0
def select(collection: list[T], func: Callable[[T], bool]):
    for item in collection:
        if func(item):
            return item
    return None

def cast_safe_get(collection: dict, key: str, type: ClassType) -> ClassType | None:
    if isinstance(collection, dict) or collection is None:
        return None

    value = collection.get(key)

    if value is None:
        return None

    return type(value)


# path = str(file.get('path'))
# imgui.add_button(label=os.path.basename(file), parent=FILE_LIST_TAG, callback=select_file, user_data=file)