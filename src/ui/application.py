import os
import xdialog

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

import src.core.control as ctrl
import src.ui.utilities as util
import src.ui.font_loader as fl

from src.core.deprecated import deprecated
from src.config.config_provider import ConfigProvider

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
    TAGS = 'tags-id'

# ======== FONT =============================
HEADLINE_FONT: int | str = ''

# ======== DATA =============================

currentDir = ''
currentFile = ''

configFiles: list[dict] = []


def init_window(*, headline_font: int | str):
    global HEADLINE_FONT
    HEADLINE_FONT = headline_font

    mw = main_window()
    pw = preview_window()
    aw = about_window()

    return [mw, aw, pw]

def main_window():
    with imgui.window(label='Main', tag=MAIN_WINDOW_ID, show=True, no_close=True, no_collapse=True, min_size=[620, 480]) as window:
        with imgui.menu_bar():
            with imgui.menu(label="File"):
                imgui.add_menu_item(label='Open...')
                imgui.add_menu_item(label='Save')
                imgui.add_menu_item(label='Save as...')

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Open directory...', callback=view_files_in_dir)

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Export...')

                util.separate_spacer(heigth=10)

                imgui.add_menu_item(label='Settings')

            with imgui.menu(label='Window'):
                imgui.add_menu_item(label='Preview', callback=lambda: show_window(PREVIEW_WINDOW_ID))
                imgui.add_menu_item(label='Tag Manager')
                imgui.add_menu_item(label='Demo', callback=demo.show_demo)
                imgui.add_menu_item(label='Dialog')

            with imgui.menu(label='Help'):
                imgui.add_menu_item(label='Docs', callback=lambda: xdialog.info('Звоните Сене!', 'Что то сломалось!? Звони Адмэну! тел: 8 800 333-35-35.'))
                imgui.add_menu_item(label='About...', callback=lambda: show_window(ABOUT_ID))

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
                        imgui.add_input_text(label='Description*', multiline=True, tag=FIELD_ID.DESCRIPTION)
                        imgui.add_input_text(label='Categories', tag=FIELD_ID.CATEGORY)
                        imgui.add_input_text(label='Release Filename', tag=FIELD_ID.RELEASE)

                        with imgui.group():
                            with imgui.group(horizontal=True):
                                imgui.add_input_text(label='')
                                imgui.add_button(label="Add")
                                imgui.add_button(label="Remove")

                            with imgui.child_window(height=40):
                                with imgui.group(horizontal=True):
                                    imgui.add_button(label='tag 1')
                                    imgui.add_button(label='tag 2')
                                    imgui.add_button(label='tag 3')
                                    imgui.add_button(label='tag 4')

                            imgui.add_spacer(height=2)

                            with imgui.child_window(height=200):
                                imgui.add_text(tag=FIELD_ID.TAGS, color=(148, 159, 47, 255), wrap=500, default_value='fdfsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddsfdddddddddddddd')

                        with imgui.group(horizontal=True):
                            imgui.add_checkbox(label='Mature content')
                            imgui.add_checkbox(label='Illustration')
                            imgui.add_checkbox(label='Editorial')

                        with imgui.group(horizontal=True):
                            imgui.add_input_float(label='Price*', width=100, step=1, step_fast=10, format='%.1f')
                            imgui.add_input_float(label='Price 2*', width=100, step=1, step_fast=10, format='%.1f')

                        imgui.add_spacer(height=10)
                        imgui.add_separator()
                        imgui.add_button(label="Set", width=-1, callback=save_value,)
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

def show_window(tag: int | str):
    imgui.show_item(tag)

def view_files_in_dir():
    files, dir_path = ctrl.show_dialog(file_types)
    if files is not None:
        render_file_view(files)

        global currentDir
        currentDir = dir_path

        f = ctrl.get_dir_config(dir_path)
        files_config = dict.get(f, 'files')
        if files_config is None:
            pass
        else:
            global configFiles
            configFiles = files_config

def save_value(sender, app_data, user_data):
    if not os.path.exists(currentFile):
        return

    filename = imgui.get_value(FIELD_ID.FILENAME)
    title = imgui.get_value(FIELD_ID.TITLE)
    description = imgui.get_value(FIELD_ID.DESCRIPTION)
    category = imgui.get_value(FIELD_ID.CATEGORY)
    release = imgui.get_value(FIELD_ID.RELEASE)
    tags = imgui.get_value(FIELD_ID.TAGS)

    if not is_valid(filename):
        print('EMPTY')
        return
    if not is_valid(title):
        print('EMPTY')
        return
    if not is_valid(description):
        print('EMPTY')
        return

    file = {
        'path': currentFile,
        'filename': filename,
        'title': title,
        'description': description,
        'category': category,
        'release_filename': release,
        'tags': ['TEST1', 'TEST2']
    }

    print(file)

    # global configFiles
    configFiles.append(file)

    ctrl.set_dir_config(currentDir, configFiles)


def render_file_view(files: list[str]):
    children = imgui.get_item_children(FILE_LIST_ID)
    print(children)

    for k, v in children.items():
        print(v)
        if v is not None:
            for i in v:
                imgui.delete_item(i)

    items = []

    for file in files:
        seletion = imgui.add_selectable(label=os.path.basename(file), parent=FILE_LIST_ID, callback=select_file, user_data=[items, file])
        items.append(seletion)

def select_file(sender, app_data, user_data):
    def _selection(items):
        for item in items:
            if item != sender:
                imgui.set_value(item, False)

    _selection(user_data[0])

    global currentFile
    currentFile = user_data[1]

    print(user_data)

    for file in configFiles:
        if file.get('path') == user_data[1]:
            path = str(file.get('path'))
            filename = str(file.get('filename'))
            title = str(file.get('title'))
            description = str(file.get('description'))
            category = str(file.get('category'))
            release = str(file.get('release_filename'))
            tags = list(file.get('tags'))

            imgui.set_value(FIELD_ID.FILENAME, filename)
            imgui.set_value(FIELD_ID.TITLE, title)
            imgui.set_value(FIELD_ID.DESCRIPTION, description)
            imgui.set_value(FIELD_ID.CATEGORY, category)
            imgui.set_value(FIELD_ID.RELEASE, release)
            imgui.set_value(FIELD_ID.TAGS, tags)
            return

    imgui.set_value(FIELD_ID.FILENAME, os.path.basename(user_data[1]))
    imgui.set_value(FIELD_ID.TITLE, '')
    imgui.set_value(FIELD_ID.DESCRIPTION, '')
    imgui.set_value(FIELD_ID.CATEGORY, '')
    imgui.set_value(FIELD_ID.RELEASE, '')
    imgui.set_value(FIELD_ID.TAGS, '')


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

def about_window():
    with imgui.window(label='About', tag=ABOUT_ID, show=False, modal=True, no_title_bar=True) as window:
        hl = imgui.add_text(default_value='Priver PIDOR')
        imgui.bind_item_font(hl, HEADLINE_FONT)
        imgui.add_button(label='Close', callback=lambda: imgui.hide_item(ABOUT_ID))

    imgui.set_item_pos(window, [300, 300])

    return window

def is_valid(value: str) -> bool:
    return value is not None and len(value) > 0


# imgui.add_button(label=os.path.basename(file), parent=FILE_LIST_TAG, callback=select_file, user_data=file)