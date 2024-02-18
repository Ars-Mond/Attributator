import os
import time
import pyperclip

import xdialog
from loguru import logger

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

import src.core.control as ctrl
import src.ui.utilities as util
import src.ui.font_loader as fl

from src.ui.color import Color
from src.core.deprecated import deprecated
from src.config.config_provider import ConfigProvider


# ========= DEFINE ===================================================
image_file_types = ['jpg', 'png']
video_file_types = ['mp4']

file_types = []
file_types.extend(image_file_types)
file_types.extend(video_file_types)

MAIN_WINDOW_ID = 'main-window-id'
SETTINGS_WINDOW_ID = 'settings-window-id'
ABOUT_ID = 'about-window-id'
PREVIEW_WINDOW_ID = 'preview-window-id'

FILE_LIST_ID = 'file-list-id'
class FIELD_ID:
    FILENAME = 'filename-id'
    TITLE = 'title-id'
    DESCRIPTION = 'description-id'
    CATEGORIES = 'categories-id'
    RELEASE = 'release-id'
    KEYWORDS = 'keywords-id'
    KEYWORDS_INPUT = 'keywords-input-id'
    KEYWORDS_ADD = 'keywords-add-id'
    KEYWORDS_REMOVE = 'keywords-remove-id'
    KEYWORDS_COPY = 'keywords-copy-id'

    MATURE_CONTENT = 'mature-id'
    ILLUSTRATION = 'illustration-id'
    EDITORIAL = 'editorial-id'

    PRICE_1 = 'price-1-id'
    PRICE_2 = 'price-2-id'

class BUTTON_ID:
    SET = 'set-button-id'
    CLEAR = 'clear-button-id'
    SAVE_PHOTO_METADATA = 'save-photo-metadata-button-id'

class TEXTURE_ID:
    CLOSE_BUTTON = 'close-texture-id'

# ========= FONT =====================================================
HEADLINE_FONT_ID: int | str = ''


# ========= DATA =====================================================
CurrentDir = ''
CurrentFilePath = ''
CurrentKeywords: list[str] = []

CurrentConfigFiles: list[dict] = []



# ========= TEST =====================================================
OLD_INPUT_TEXT_VALUE = ''


# ========= WINDOWS ==================================================
def init_window(*, headline_font: int | str) -> tuple[int | str]:
    global HEADLINE_FONT_ID
    HEADLINE_FONT_ID = headline_font

    _theme_init()

    mw = main_window()
    pw = preview_window()
    sw = settings_window()
    aw = about_window()

    logger.info('Inited windows')

    return mw, pw, sw, aw

def _theme_init():
    c = Color('b4c569')
    print(c.get_RGBA())

    with imgui.theme(tag='__ok_feel'):
        with imgui.theme_component(imgui.mvButton):
            imgui.add_theme_color(imgui.mvThemeCol_Button, c.get_RGBA())
            imgui.add_theme_color(imgui.mvThemeCol_ButtonActive, c.get_RGBA())
            imgui.add_theme_color(imgui.mvThemeCol_ButtonHovered, c.get_RGBA())


@logger.catch
def main_window():
    with imgui.window(label='Main', tag=MAIN_WINDOW_ID, show=True, no_close=True, no_collapse=True, min_size=[620, 480]) as window:
        with imgui.menu_bar():
            with imgui.menu(label="File"):
                imgui.add_menu_item(label='Open directory...', callback=_show_directiry_dialog)

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Export...', callback=_export_button)

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Settings', callback=lambda: _show_window_center(SETTINGS_WINDOW_ID))

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

                with imgui.table_cell() as cell:
                    imgui.add_text(default_value="Tools")
                    with imgui.child_window(height=-15):
                        imgui.add_input_text(label='Filename*', tag=FIELD_ID.FILENAME, width=-200)
                        imgui.add_input_text(label='Title*', tag=FIELD_ID.TITLE, width=-200)
                        imgui.add_input_text(label='Description*', tag=FIELD_ID.DESCRIPTION, multiline=True, width=-200)
                        imgui.add_input_text(label='Categories', tag=FIELD_ID.CATEGORIES, width=-200)
                        _help_last('Categories.')
                        imgui.add_input_text(label='Release filename', tag=FIELD_ID.RELEASE, width=-200)
                        _help_last('Release filename.')

                        imgui.add_spacer(height=2)
                        imgui.add_separator()

                        imgui.add_text(default_value='Keywords:')
                        with imgui.group(horizontal=True):
                            imgui.add_input_text(tag=FIELD_ID.KEYWORDS_INPUT, width=-200)
                            imgui.add_button(label='Add', tag=FIELD_ID.KEYWORDS_ADD, callback=_add_keywords_button)
                            imgui.add_button(label='Remove', tag=FIELD_ID.KEYWORDS_REMOVE, callback=_remove_keywords_button)
                            imgui.add_button(label='Copy All', tag=FIELD_ID.KEYWORDS_COPY, callback=_copy_keywords_button)

                        with imgui.child_window(height=200):
                            imgui.add_text(label='Keywords*:', tag=FIELD_ID.KEYWORDS, wrap=0)

                        imgui.add_separator()

                        imgui.add_spacer(height=1)

                        with imgui.tree_node(label='Advanced'):
                            with imgui.group(horizontal=True):
                                imgui.add_checkbox(label='Mature content', tag=FIELD_ID.MATURE_CONTENT)
                                imgui.add_checkbox(label='Illustration', tag=FIELD_ID.ILLUSTRATION)
                                imgui.add_checkbox(label='Editorial', tag=FIELD_ID.EDITORIAL)

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

                        imgui.add_button(label="Save", width=-1, callback=_save_button)
                        imgui.add_button(label="Clear", width=-1, callback=_clear_button)

                        imgui.add_spacer(height=20)

                        imgui.add_button(label="Save photo metadata", tag=BUTTON_ID.SAVE_PHOTO_METADATA, width=-1)

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

def settings_window():
    with imgui.window(label='Settings', tag=SETTINGS_WINDOW_ID, min_size=[640, 480], show=False, modal=True, no_collapse=True, no_close=True) as window:
        imgui.add_text(default_value='Coming soon.')

        with imgui.group(horizontal=True):
            imgui.add_button(label="Save")
            imgui.add_button(label="Cancel", callback=lambda: imgui.hide_item(SETTINGS_WINDOW_ID))
        pass

    return window

def about_window():
    with imgui.window(label='About', tag=ABOUT_ID, min_size=[640, 480], show=False, modal=True, no_title_bar=True) as window:
        hl = imgui.add_text(default_value='Priver')
        imgui.bind_item_font(hl, HEADLINE_FONT_ID)
        imgui.add_button(label='Close', callback=lambda: imgui.hide_item(ABOUT_ID))

    imgui.set_item_pos(window, [300, 300])

    return window

def _add_keywords_button(sender, app_data, user_data):
    if _check_can_edit():
        return

    s: str = imgui.get_value(FIELD_ID.KEYWORDS_INPUT)
    if len(s) <= 0: return

    s = s.encode('cp1252').decode('cp1251')

    keywords = ctrl.get_items_format(s)

    for keyword in keywords:
        if not keyword in CurrentKeywords:
            CurrentKeywords.append(keyword)
    CurrentKeywords.sort()

    logger.info(f'Try add keyword(s): {keywords}')
    logger.debug(f'Current keywords: {CurrentKeywords}')

    imgui.set_value(FIELD_ID.KEYWORDS_INPUT, '')
    imgui.set_value(FIELD_ID.KEYWORDS, ', '.join(CurrentKeywords))

    _click_feel(sender, 0.2)

def _remove_keywords_button(sender, app_data, user_data):
    if _check_can_edit():
        return

    s: str = imgui.get_value(FIELD_ID.KEYWORDS_INPUT)
    if len(s) <= 0:
        return

    keywords = ctrl.get_items_format(s)

    for keyword in keywords:
        if keyword in CurrentKeywords:
            CurrentKeywords.remove(keyword)
    CurrentKeywords.sort()

    logger.info(f'Try remove keyword(s): {keywords}')
    logger.debug(f'Current keywords: {CurrentKeywords}')

    imgui.set_value(FIELD_ID.KEYWORDS_INPUT, '')
    imgui.set_value(FIELD_ID.KEYWORDS, ', '.join(CurrentKeywords))

    _click_feel(sender, 0.2)

def _copy_keywords_button(sender, app_data, user_data):
    if _check_can_edit():
        return

    if CurrentKeywords is not None and len(CurrentKeywords) > 0:
        text = ', '.join(CurrentKeywords)
        pyperclip.copy(text)
        logger.debug(f'Copy text to clipboard: {text}')
        _click_feel(sender, 0.5)

def _save_button(sender, app_data, user_data):
    if _check_can_edit():
        return

    filename, title, description, categories, release, keywords, mature_content, illustration, editorial, price1, price2 = _get_attributes_view()

    if not ctrl.is_valid(filename):
        logger.warning('The "filename" field is not filled in.')
        _show_error("Field error", 'The "filename" field is not filled in.')
        return
    if not ctrl.is_valid(title):
        logger.warning('The "title" field is not filled in.')
        _show_error("Field error", 'The "title" field is not filled in.')
        return
    if not ctrl.is_valid(description):
        logger.warning('The "description" field is not filled in.')
        _show_error("Field error", 'The "description" field is not filled in.')
        return
    if not ctrl.is_valid(keywords):
        logger.warning('The "keyword(s)" field is not filled in.')
        _show_error("Field error", 'The "keywords" field is not filled in.')
        return

    new_file_data = {
        'path': CurrentFilePath,
        'filename': filename,
        'title': title,
        'description': description,
        'categories': categories,
        'release_filename': release,
        'keywords': keywords,
        'mature_content': mature_content,
        'illustration': illustration,
        'editorial': editorial,
        'price1': price1,
        'price2': price2,
    }

    for file in CurrentConfigFiles:
        if file.get('path') == CurrentFilePath:
            CurrentConfigFiles.remove(file)
            logger.info(f'Save data: {file}')
            break

    # global configFiles
    CurrentConfigFiles.append(new_file_data)

    ctrl.set_dir_config(CurrentDir, {'files': CurrentConfigFiles})

    _click_feel(sender, 0.7)

def _clear_button(sender, app_data, user_data):
    if _check_can_edit():
        return

    imgui.set_value(FIELD_ID.TITLE, '')
    imgui.set_value(FIELD_ID.DESCRIPTION, '')
    imgui.set_value(FIELD_ID.CATEGORIES, '')
    imgui.set_value(FIELD_ID.RELEASE, '')
    imgui.set_value(FIELD_ID.KEYWORDS, '')

    imgui.set_value(FIELD_ID.MATURE_CONTENT, False)
    imgui.set_value(FIELD_ID.ILLUSTRATION, False)
    imgui.set_value(FIELD_ID.EDITORIAL, False)
    imgui.set_value(FIELD_ID.PRICE_1, 0.0)
    imgui.set_value(FIELD_ID.PRICE_2, 0.0)

    _set_attributes_view('None',
                         '',
                         '',
                         '',
                         '',
                         '',
                         False,
                         False,
                         False,
                         0.0,
                         0.0)

    global CurrentKeywords
    CurrentKeywords = []

    for file in CurrentConfigFiles:
        if file.get('path') == CurrentFilePath:
            CurrentConfigFiles.remove(file)
            logger.info(f'Clear data: {file}')
            break

    ctrl.set_dir_config(CurrentDir, {'files': CurrentConfigFiles})

    _click_feel(sender, 0.7)

def _show_directiry_dialog():
    alle = ctrl.show_dialog(file_types)
    if alle is None:
        _hide_files_list()
        _show_error('Directory', 'Directory is none!')
        return

    _show_files_list(alle[0], alle[1])

def _show_files_list(files, dir_path):
    if files is not None:
        _render_file_view(files)

        global CurrentDir
        CurrentDir = dir_path

        f = ctrl.get_dir_config(dir_path)

        if f is None:
            return

        files_config = dict.get(f, 'files')
        if files_config is not None:
            global CurrentConfigFiles
            CurrentConfigFiles = files_config

def _hide_files_list():
    _render_file_view([])

    global CurrentDir
    CurrentDir = ''

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
    logger.debug(f'Select file: {sender} | {app_data} | {user_data}')
    def _selection(items):
        for item in items:
            if item != sender:
                imgui.set_value(item, False)

    _selection(user_data[0])

    global CurrentFilePath

    if CurrentFilePath == user_data[1]:
        return

    CurrentFilePath = user_data[1]

    global CurrentKeywords
    CurrentKeywords = []

    file = ctrl.select(CurrentConfigFiles, lambda item: item.get('path') == user_data[1])

    if file is not None:
        logger.info(f'File data found. {file.get('path')}')

        filename = ctrl.cast_safe_get(file, 'filename', str)
        title = ctrl.cast_safe_get(file, 'title', str)
        description = ctrl.cast_safe_get(file, 'description', str)
        categories = ctrl.cast_safe_get(file, 'categories', str)
        release = ctrl.cast_safe_get(file, 'release', str)
        keywords = ctrl.cast_safe_get(file, 'keywords', list)

        mature_content = ctrl.cast_safe_get(file, 'mature_content', bool)
        illustration = ctrl.cast_safe_get(file, 'illustration', bool)
        editorial = ctrl.cast_safe_get(file, 'editorial', bool)
        price1 = ctrl.cast_safe_get(file, 'price1', float)
        price2 = ctrl.cast_safe_get(file, 'price2', float)

        if filename is not None: imgui.set_value(FIELD_ID.FILENAME, filename)
        if title is not None: imgui.set_value(FIELD_ID.TITLE, title)
        if description is not None: imgui.set_value(FIELD_ID.DESCRIPTION, description)
        if categories is not None: imgui.set_value(FIELD_ID.CATEGORIES, categories)
        if release is not None: imgui.set_value(FIELD_ID.RELEASE, release)
        if keywords is not None: imgui.set_value(FIELD_ID.KEYWORDS, ', '.join(keywords))

        if mature_content is not None: imgui.set_value(FIELD_ID.MATURE_CONTENT, mature_content)
        if illustration is not None: imgui.set_value(FIELD_ID.ILLUSTRATION, illustration)
        if editorial is not None: imgui.set_value(FIELD_ID.EDITORIAL, editorial)
        if price1 is not None: imgui.set_value(FIELD_ID.PRICE_1, price1)
        if price2 is not None: imgui.set_value(FIELD_ID.PRICE_2, price2)

        CurrentKeywords = keywords
        return


    imgui.set_value(FIELD_ID.FILENAME, os.path.basename(user_data[1]))
    imgui.set_value(FIELD_ID.TITLE, '')
    imgui.set_value(FIELD_ID.DESCRIPTION, '')
    imgui.set_value(FIELD_ID.CATEGORIES, '')
    imgui.set_value(FIELD_ID.RELEASE, '')
    imgui.set_value(FIELD_ID.KEYWORDS, '')

    imgui.set_value(FIELD_ID.MATURE_CONTENT, False)
    imgui.set_value(FIELD_ID.ILLUSTRATION, False)
    imgui.set_value(FIELD_ID.EDITORIAL, False)
    imgui.set_value(FIELD_ID.PRICE_1, 0.0)
    imgui.set_value(FIELD_ID.PRICE_2, 0.0)

def _export_button(sender, app_data, user_data):
    if _check_can_edit(False):
        return

    path = xdialog.directory('Select a folder to save...')
    if path is None or not os.path.exists(path):
        return

    data = ctrl.get_dir_config(CurrentDir)

    datas: list[ctrl.FileData] = ctrl.FileData.create_many_from_files(data)

    new_datas = []
    for data in datas:
        if data.filename.split('.')[1] in video_file_types:
            new_datas.append(data)

    if len(new_datas) <= 0:
        xdialog.info('Data(s) doesn\'t exist', 'Video file(s) data(s) doesn\'t exist.')
        return

    ctrl.export_csv(path, datas, True)



# ========= UTILITIES ================================================

def _get_attributes_view() -> tuple[str, str, str, str, str, list[str], bool, bool, bool, float, float]:
    filename: str = imgui.get_value(FIELD_ID.FILENAME)
    title: str = imgui.get_value(FIELD_ID.TITLE)
    description: str = imgui.get_value(FIELD_ID.DESCRIPTION)
    categories: str = imgui.get_value(FIELD_ID.CATEGORIES)
    release: str = imgui.get_value(FIELD_ID.RELEASE)
    keywords: list[str] = CurrentKeywords  # keywords = imgui.get_value(FIELD_ID.KEYWORDS)

    mature_content: bool = imgui.get_value(FIELD_ID.MATURE_CONTENT)
    illustration: bool = imgui.get_value(FIELD_ID.ILLUSTRATION)
    editorial: bool = imgui.get_value(FIELD_ID.EDITORIAL)
    price1: float = imgui.get_value(FIELD_ID.PRICE_1)
    price2: float = imgui.get_value(FIELD_ID.PRICE_2)

    return filename, title, description, categories, release, keywords, mature_content, illustration, editorial, price1, price2


def _set_attributes_view(filename: str | None = None,
                         title: str | None = None,
                         description: str | None = None,
                         categories: str | None = None,
                         release: str | None = None,
                         keywords: str | list[str] | None = None,
                         mature_content: bool | None = None,
                         illustration: bool | None = None,
                         editorial: bool | None = None,
                         price1: float | None = None,
                         price2: float | None = None) -> None:
    if isinstance(keywords, list):
        keywords = ', '.join(keywords)

    if filename is not None: imgui.set_value(FIELD_ID.FILENAME, filename)
    if title is not None: imgui.set_value(FIELD_ID.TITLE, title)
    if description is not None: imgui.set_value(FIELD_ID.DESCRIPTION, description)
    if categories is not None: imgui.set_value(FIELD_ID.CATEGORIES, categories)
    if release is not None: imgui.set_value(FIELD_ID.RELEASE, release)
    if keywords is not None: imgui.set_value(FIELD_ID.KEYWORDS, keywords)

    if mature_content is not None: imgui.set_value(FIELD_ID.MATURE_CONTENT, mature_content)
    if illustration is not None: imgui.set_value(FIELD_ID.ILLUSTRATION, illustration)
    if editorial is not None: imgui.set_value(FIELD_ID.EDITORIAL, editorial)
    if price1 is not None: imgui.set_value(FIELD_ID.PRICE_1, price1)
    if price2 is not None: imgui.set_value(FIELD_ID.PRICE_2, price2)


def _log(sender, app_data, user_data):
    logger.debug(f'{sender} | {app_data} | {user_data}')

def _show_window(tag: int | str):
    imgui.show_item(tag)

def _show_window_center(tag: int | str):
    imgui.show_item(tag)

    viewport_size = [imgui.get_viewport_width(), imgui.get_viewport_height()]
    item_size = imgui.get_item_rect_size(tag)


    pos = [int(viewport_size[0] / 2 - item_size[0] / 2), int(viewport_size[1] / 2 - item_size[1] / 2)]

    imgui.set_item_pos(tag, pos)

def _show_error(title: str, message: str):
    return xdialog.error(title, message)

def _help_last(message: str | list[str], join_str: str = '\n'):
    last_item = imgui.last_item()
    _help(last_item, message, join_str)

def _help(tag: int | str, message: str | list[str], join_str: str = '\n'):
    temp_message = message
    if isinstance(message, list):
        temp_message = join_str.join(message)

    parent = imgui.get_item_parent(tag)
    group = imgui.add_group(horizontal=True, parent=parent)
    imgui.move_item(tag, parent=group)
    imgui.capture_next_item(lambda s: imgui.move_item(s, parent=group))
    t = imgui.add_text("(?)", color=[0, 255, 0])
    with imgui.tooltip(t):
        imgui.add_text(temp_message)

def _click_feel(tag: int | str, delta: float):
    imgui.bind_item_theme(tag, '__ok_feel')
    time.sleep(delta)
    imgui.bind_item_theme(tag, 0)

def _check_can_edit(is_all_context: bool = True) -> bool:
    b = not os.path.exists(CurrentDir) or not os.path.exists(CurrentFilePath)
    if not is_all_context:
        b = not os.path.exists(CurrentDir)
    if b:
        xdialog.warning('Context doesn\'t exist', 'The working context is not selected or does not exist!')
    return b

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

# w_close_button, h_close_button, c_close_button, d_close_button = imgui.load_image(os.path.abspath('./data/images/close2.png'))
#
#     with imgui.texture_registry(show=False):
#         imgui.add_static_texture(width=w_close_button, height=h_close_button, default_value=d_close_button, tag=TEXTURE_ID.CLOSE_BUTTON)


# imgui.add_menu_item(label='Open...')
# imgui.add_menu_item(label='Save')
# imgui.add_menu_item(label='Save as...')
#
# util.separate_spacer(heigth=10)


# path = str(file.get('path'))
# imgui.add_button(label=os.path.basename(file), parent=FILE_LIST_TAG, callback=select_file, user_data=file)

#     with imgui.theme(tag='__test'):
#         with imgui.theme_component(imgui.mvText):
#             c = Color('#ada')
#             print(c.get_RGBA())
#             imgui.add_theme_color(imgui.mvThemeCol_Text, c.get_RGBA())

# imgui.bind_item_theme(g, '__test')


# with imgui.group(horizontal=True):
#     for i in range(20):
#         with imgui.group(horizontal=True) as group:
#             imgui.add_text(default_value=f'item {i}')
#             imgui.add_image_button(TEXTURE_ID.CLOSE_BUTTON, width=6, height=6)

# imgui.add_input_text(label='Keywords*', tag=FIELD_ID.KEYWORDS, multiline=True, callback=wrap_input_text, on_enter=True)


# datas: list[ctrl.FileData] = ctrl.FileData.create_many(data)

# data = data.get('files')
# logger.debug(data)
