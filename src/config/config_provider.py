import yaml
import os


class ConfigProvider:
    path_file: str
    name_file: str
    path_data_dir: str | None

    def __init__(self, path_file: str, name_file: str, path_data_dir: str | None = None):
        self.path_file = path_file
        self.name_file = name_file
        self.path_data_dir = path_data_dir

    def get_all(self):
        config = self.__load_config()

        if config is None:
            return None

        return config

    def get_value(self, name_value: str):
        config = self.__load_config()

        if config is None:
            return None

        return dict.get(config, name_value)

    def set_value(self, name_value: str, value: any):
        config = self.__load_config()

        if type(config) is dict:
            config = dict(config)

        else:
            config = dict()

        config[name_value] = value
        self.__save_config(config)

    def is_value(self, name_value: str):
        config = self.__load_config()
        return config.get(name_value) is not None

    def try_set_value(self, name_value: str, value: any, exist: bool = False):
        config = self.__load_config()

        if type(config) is dict:
            config = dict(config)

        else:
            config = dict()

        if not (exist ^ (config.get(name_value) is not None)):
            config[name_value] = value
            self.__save_config(config)
        else:
            e = "The value doesn't exist." if exist else "The value exist."
            raise ValueError(e)
        pass

    def get_or_create_config(self, write: bool = False):
        path_dir = self.get_or_create_dir()

        path = os.path.join(path_dir, self.name_file + '.yml')
        if os.path.isfile(path) is False:
            open(path, 'x').close()

        ex = 'wt' if write else 'rt'
        return open(path, ex)

    def get_or_create_dir(self):
        path = os.path.join(self.path_data_dir, self.path_file) if self.can_use_data() else self.path_file
        path = os.path.abspath(path)

        if os.path.isdir(path) is False:
            os.makedirs(path)
        return path

    def can_use_data(self) -> bool:
        return self.path_data_dir is not None

    def __load_config(self):
        file = self.get_or_create_config(write=False)
        config_data = yaml.load(stream=file, Loader=yaml.FullLoader)
        return config_data

    def __save_config(self, data: any):
        file = self.get_or_create_config(write=True)
        yaml.dump(data, file, default_flow_style=False)
