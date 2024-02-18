import os
import re
import xdialog

from schema import Schema, And, Use, Optional, SchemaError

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

from typing import Callable, TypeVar

T = TypeVar('T')
ClassType = TypeVar('ClassType')

from src.config.config_provider import ConfigProvider

cp = ConfigProvider('', '')


def show_dialog(file_types: list[str]) -> dict[str] | None:
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
        return None
        # set_dir_config(dir_path, {}, dir_name=dir_name, config_name=config_name)
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


dir_config_signature = Schema({
    Optional('files'): [
        {
            'filename': str,
            'release_filename': str,
            'title': str,
            'descriprion': str,
            Optional('categories'): str,
            'keywords': str,
            Optional('mature_content'): bool,
            Optional('illustration'): bool,
            Optional('editorial'): bool,
            Optional('price1'): float | int,
            Optional('price2'): float | int
        }
    ]
})


def is_valid(value: str | list) -> bool:
    return value is not None and len(value) > 0
def select(collection: list[T], func: Callable[[T], bool]):
    for item in collection:
        if func(item):
            return item
    return None

def cast_safe_get(collection: dict, key: str, type: ClassType) -> ClassType | None:
    if not isinstance(collection, dict) or collection is None:
        return None

    value = collection.get(key)

    if value is None:
        return None

    return type(value)

def get_items_format(value: str, *, split_char: str = ',', clerar_chars: str = ' ', is_lower: bool = True) -> list[str]:
    value = value.replace('\n', ' ').replace('\t', ' ')
    value = re.sub(r'[^A-Za-z\s]*', '', value) # r'[.*\[\]{}!?@#$%^&()_+\-=|\\/><\"\'1234567890:;№]+'
    value = re.sub('\\s{2,}', ' ', value)
    temp_values = value.split(split_char)
    collection: list[str] = []

    for temp_value in temp_values:
        temp_value = temp_value.strip(clerar_chars)

        if is_lower:
            temp_value = temp_value.lower()

        if len(temp_value) > 0:
            collection.append(temp_value)

    return collection








# dir_config_signature = Schema({
#     Optional('files'): [
#         {
#             'filename': str,
#             'release_filename': str,
#             'title': str,
#             'descriprion': str,
#             Optional('categories'): str,
#             'keywords': list[str]
#         }
#     ]
# })