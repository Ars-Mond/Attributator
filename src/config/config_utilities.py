from src.config.config_provider import ConfigProvider

last_id_db = 'last_id'
catalogs_db = 'catalogs'
id_db = 'id'
name_db = 'name'
description_db = 'description'
url_db = 'url'
images_db = 'images'
src_db = 'src'
alt_db = 'alt'


def get_items(list_value: list, name_item: str):
    res = []
    for item in list_value:
        if type(item) is not dict:
            continue
        if name_item in item:
            res.append(item[name_item])
    return res


def find(elements: list, name_item: str, value_item):
    res = []
    for element in elements:
        if type(element) is not dict:
            continue
        if name_item in element and value_item is element[name_item]:
            res.append(element)
    return res


def exist(elements: list, name_item: str, value):
    for element in elements:
        if type(element) is not dict:
            continue
        if value == element.get(name_item):
            return True
    return False

# return [item for item in get_items(list_value, name_item) if value_item in item]


def get_catalog(cp: ConfigProvider):
    return cp.get_value(catalogs_db)