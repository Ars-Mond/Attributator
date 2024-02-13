import os
import xdialog

from schema import Schema, And, Use, Optional, SchemaError

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

from src.config.config_provider import ConfigProvider

cp = ConfigProvider('', '')

def show_dialog(file_types: list[str]) -> list[str] | None:
    dir_path = xdialog.directory()

    if dir_path is not None and os.path.exists(dir_path):
        files = []
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            if not os.path.isfile(file_path): continue;
            if not os.path.basename(file_path).split('.')[1] in file_types: continue;

            files.append(file_path)
        return files, dir_path

    return None

def get_dir_config(dir_path: str, *, dir_name: str = '_attrs', config_name: str = '_files') -> dict | None:
    path_dir = os.path.join(dir_path, dir_name)

    if not os.path.exists(path_dir):
        set_dir_config(dir_path, {}, dir_name=dir_name, config_name=config_name)
        # raise Exception()

    cp.path_file = path_dir
    cp.name_file = config_name

    return cp.get_value('all')


def set_dir_config(dir_path: str, data: dict, *, dir_name: str = '_attrs', config_name: str = '_files') -> None:
    path_dir = os.path.join(dir_path, dir_name)

    # if not os.path.exists(path_dir):
    #     raise Exception()

    cp.path_file = path_dir
    cp.name_file = config_name

    cp.set_value('all', data)


def get_signature() :
    pass


dir_config_signature = Schema({
    'all': {
        Optional('files'): [
            {
                'filename': str,
                'release_filename': str,
                'title': str,
                'descriprion': str,
                Optional('categories'): str,
                'tags': list[str]
            }
        ]
    }
})
