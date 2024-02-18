import os
import re
import xdialog

from loguru import logger

from schema import Schema, And, Use, Optional, SchemaError

import dearpygui.dearpygui as imgui
import dearpygui.demo as demo

from typing import Callable, TypeVar

T = TypeVar('T')
ClassType = TypeVar('ClassType')


class FileData:
    class FIELD_NAME:
        FILES = 'files'

        PATH = 'path'

        FILENAME = 'filename'
        TITLE = 'title'
        DESCRIPTION = 'description'
        CATEGORIES = 'categories'
        RELEASE_FILENAME = 'release_filename'
        KEYWORDS = 'keywords'
        MATURE_CONTENT = 'mature_content'
        ILLUSTRATION = 'illustration'
        EDITORIAL = 'editorial'
        PRICE1 = 'price1'
        PRICE2 = 'price2'

    SIGNATURE = Schema({
        FIELD_NAME.PATH: str,

        FIELD_NAME.FILENAME: str,
        FIELD_NAME.TITLE: str,
        FIELD_NAME.DESCRIPTION: str,
        Optional(FIELD_NAME.CATEGORIES): str,
        Optional(FIELD_NAME.RELEASE_FILENAME): str,
        FIELD_NAME.KEYWORDS: list,
        Optional(FIELD_NAME.MATURE_CONTENT): bool,
        Optional(FIELD_NAME.ILLUSTRATION): bool,
        Optional(FIELD_NAME.EDITORIAL): bool,
        Optional(FIELD_NAME.PRICE1): float,
        Optional(FIELD_NAME.PRICE2): float
    })
    SIGNATURE_LIST = Schema({
        Optional(FIELD_NAME.FILES): [
            SIGNATURE
        ]
    })
    def __init__(self,
                 filename: str | None = None,
                 title: str | None = None,
                 description: str | None = None,
                 categories: str | None = None,
                 release: str | None = None,
                 keywords: list[str] | None = None,
                 mature_content: bool | None = None,
                 illustration: bool | None = None,
                 editorial: bool | None = None,
                 price1: float | None = None,
                 price2: float | None = None,
                 path: str | None = None):
        self.filename: str | None = filename
        self.title: str | None = title
        self.description: str | None = description
        self.categories: str | None = categories
        self.release: str | None = release
        self.keywords: list[str] | None = keywords
        self.mature_content: bool | None = mature_content
        self.illustration: bool | None = illustration
        self.editorial: bool | None = editorial
        self.price1: float | None = price1
        self.price2: float | None = price2

        self.path: str | None = path

    @staticmethod
    @logger.catch
    def create_one(raw: dict):
        if not FileData.SIGNATURE.is_valid(raw):
            FileData.SIGNATURE.validate(raw)
            raise Exception()

        return FileData(raw.get(FileData.FIELD_NAME.FILENAME),
                        raw.get(FileData.FIELD_NAME.TITLE),
                        raw.get(FileData.FIELD_NAME.DESCRIPTION),
                        raw.get(FileData.FIELD_NAME.CATEGORIES),
                        raw.get(FileData.FIELD_NAME.RELEASE_FILENAME),
                        raw.get(FileData.FIELD_NAME.KEYWORDS),
                        raw.get(FileData.FIELD_NAME.MATURE_CONTENT),
                        raw.get(FileData.FIELD_NAME.ILLUSTRATION),
                        raw.get(FileData.FIELD_NAME.EDITORIAL),
                        raw.get(FileData.FIELD_NAME.PRICE1),
                        raw.get(FileData.FIELD_NAME.PRICE2))

    @staticmethod
    def create_many(raw: list[dict]):
        out: list[FileData] = []
        for item in raw:
            out.append(FileData.create_one(item))

        return out

    @staticmethod
    @logger.catch
    def create_many_from_files(raw: dict[dict]):
        if not FileData.SIGNATURE_LIST.is_valid(raw):
            FileData.SIGNATURE_LIST.validate(raw)
            raise Exception()

        raw: list[dict] = raw.get(FileData.FIELD_NAME.FILES)

        out: list[FileData] = []
        for item in raw:
            out.append(FileData.create_one(item))

        return out


import src.csv.csv_stocks as csv_stocks
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


def export_csv(out_dir_path: str, datas: list[FileData], craete_dir: bool = False):
    if not os.path.exists(out_dir_path) or not os.path.isdir(out_dir_path):
        raise Exception()

    if craete_dir:
        out_dir_path = os.path.join(out_dir_path, 'export')
        if os.path.exists(out_dir_path):
            raise Exception()

        os.makedirs(out_dir_path)

    csv_stocks.create_shutterstock_csv(out_dir_path, 'shutterstock', datas)
    csv_stocks.create_istock_csv(out_dir_path, 'istock', datas)
    csv_stocks.create_adobestock_csv(out_dir_path, 'adobestock', datas)


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
    value = re.sub(r'[^A-Za-z\s,]*', '', value) # r'[.*\[\]{}!?@#$%^&()_+\-=|\\/><\"\'1234567890:;№]+'
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
#             'description': str,
#             Optional('categories'): str,
#             'keywords': list[str]
#         }
#     ]
# })


SIGNATURE = Schema({
    'filename': str,
    'release_filename': str,
    'title': str,
    'description': str,
    Optional('categories'): str,
    'keywords': list,
    Optional('mature_content'): bool,
    Optional('illustration'): bool,
    Optional('editorial'): bool,
    Optional('price1'): float,
    Optional('price2'): float})
SIGNATURE_LIST = Schema({
    Optional('files'): [SIGNATURE]})

g = {'files': [{'categories': 'nature',
                'description': 'Quite boy those. Shoulder future fall citizen about. Will seven medical blood personal.\nCurrent hear claim well two truth out major. Upon these story film. Drive note bad rule.',
                'editorial': False, 'filename': 'photomode_01082023_050104.png', 'illustration': False,
                'keywords': ['hello', 'qwerty', 'rom'], 'mature_content': False,
                'path': 'C:\\Users\\Ars_Mond\\Pictures\\Cyberpunk 2077\\photomode_01082023_050104.png', 'price1': 0.0,
                'price2': 0.0, 'release_filename': '', 'title': 'Images'}]}
