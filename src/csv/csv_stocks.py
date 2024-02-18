import csv
import os

from io import TextIOWrapper
from loguru import logger

from src.core.control import FileData

DIALECT_NAME = 'stock_dialect'

csv.register_dialect(DIALECT_NAME, delimiter=',', quotechar='"')
def create_shutterstock_csv(file_path: str, file_name: str, file_datas: list[FileData]):
    full_path = os.path.abspath(os.path.join(file_path, file_name + '.csv'))

    if os.path.exists(full_path):
        raise Exception()

    new_data: list = [['Filename', 'Description', 'Keywords', 'Categories', 'Editorial', 'Mature content', 'Illustration']]
    for file_data in file_datas:
        new_data.append([file_data.filename,
                         file_data.description,
                         ', '.join(file_data.keywords),
                         file_data.categories,
                         'yes' if file_data.editorial else 'no',
                         'yes' if file_data.mature_content else 'no',
                         'yes' if file_data.illustration else 'no'])

    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, dialect=DIALECT_NAME)
        writer.writerows(new_data)

    return full_path, file


def create_istock_csv(file_path: str, file_name: str, file_datas: list[FileData]):
    full_path = os.path.abspath(os.path.join(file_path, file_name + '.csv'))

    if os.path.exists(full_path):
        raise Exception()

    new_data: list = [['file name', 'description', 'country', 'title', 'keywords', 'poster timecode', 'date created', 'shot speed']]
    for file_data in file_datas:
        new_data.append([file_data.filename,
                         file_data.description,
                         'austria',
                         file_data.title,
                         ', '.join(file_data.keywords),
                         None,
                         None,
                         None])

    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, dialect=DIALECT_NAME)
        writer.writerows(new_data)

    return full_path, file

def create_adobestock_csv(file_path: str, file_name: str, file_datas: list[FileData]):
    full_path = os.path.abspath(os.path.join(file_path, file_name + '.csv'))

    if os.path.exists(full_path):
        raise Exception()

    new_data: list = [['Filename', 'Title', 'Keywords', 'Category', 'Releases']]
    for file_data in file_datas:
        logger.debug(file_data)
        new_data.append([file_data.filename,
                         file_data.title,
                         ', '.join(file_data.keywords),
                         0,
                         file_data.release])

    with open(full_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, dialect=DIALECT_NAME)
        writer.writerows(new_data)

    return full_path, file