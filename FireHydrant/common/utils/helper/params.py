import json
from common.exceptions.common.paramsExcept import ParamsExcept

class ParamsParser(object):

    def __init__(self, query_set):
        """
        初始化
        :param query_set: 查询集
        """
        self.query_set = query_set
        self.raw_object = None
        self.diff_mode = False

    def diff(self, raw):
        """
        启动diff模式
        :param raw:
        :return:
        """
        self.raw_object = raw
        self.diff_mode = True
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.raw_object = None
        self.diff_mode = False

    def __get_raw_object_value(self, key):
        """
        获取原始数据
        :param key:
        :return:
        """
        if self.raw_object is not None:
            # 兼容dict
            if isinstance(self.raw_object, dict):
                return self.raw_object.get(key, None)
            # 兼容Query
            elif isinstance(self.raw_object, object):
                if hasattr(self.raw_object, key):
                    return getattr(self.raw_object, key)

        return None

    def __get_value(self, key, desc='', require=False, type=object, default=None):
        """
        获取数据
        :param key:
        :param desc:
        :param require:
        :param type:
        :param default:
        :return:
        """
        value = self.query_set.get(key, None)

        if (not self.diff_mode) and require and value is None or str(value).strip() == '' :
            raise ParamsExcept.parameter_none_error(key)

        if value is None:
            value = self.__get_raw_object_value(key)
            if value is None:
                if isinstance(default, type):
                    value = default

        return value

    def has(self, key):
        """
        判断是否有对应元素
        :param key:
        :return:
        """
        return self.query_set.get(key, None) is not None

    def int(self, key, desc='', require=True, default=0):
        """
        解析int
        :param key:
        :param desc:
        :param require:
        :param default:
        :return:
        """
        value = self.__get_value(key, desc, require, int, default)

        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise ParamsExcept.parameter_int_error()

        return value

    def float(self, key, desc='', require=True, default=0.0):
        """
        解析float
        :param key:
        :param desc:
        :param require:
        :param default:
        :return:
        """
        value = self.__get_value(key, desc, require, float, default)

        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise ParamsExcept.parameter_float_error()

        return value

    def str(self, key, desc='', require=True, default=''):
        """
        解析str
        :param key:
        :param desc:
        :param require:
        :param default:
        :return:
        """
        value = self.__get_value(key, desc, require, str, default)

        if not isinstance(value, str):
            try:
                value = str(value)
            except:
                raise ParamsExcept.parameter_str_error()

        return value

    def bool(self, key, desc='', require=True, default=False):
        """
        解析为bool
        :param key: keyword。
        :param desc: 字段说明，用于抛出异常时的映射
        :param require: 必须字段，True时在没有获取到内容的时抛出异常
        :param default: 默认值，在取值为None时替换
        :return:
        """
        value = self.__get_value(key, desc, require, bool, default)

        if not isinstance(value, bool):
            if str(value).lower() in ['true', '1', 'yes', 'on']:
                x = True
            else:
                x = False
        else:
            x = value

        return x

    def list(self, key, desc='', require=True, default=None):
        """
        解析list
        :param key:
        :param desc:
        :param require:
        :param default:
        :return:
        """
        # list不支持在diff模式下使用
        if self.diff_mode:
            raise ParamsExcept.model_diff_error()

        try:
            if hasattr(self.query_set, 'getlist'):
                value = self.query_set.getlist(key, None)
            else:
                value = self.query_set.get(key, None)
        except:
            value = None

        if require and (value is None):
            raise ParamsExcept.parameter_list_error()

        # 赋予默认值(在value为None或者不是一个列表的时候）
        if not require and (value is None or not isinstance(value, list)):
            if isinstance(default, list):
                return default
            else:
                return list()

        return value

    def dict(self, key, desc='', require=True, default=None):
        """
        解析为dict
        :param key:
        :param desc:
        :param require:
        :param default:
        :return:
        """
        value = self.__get_value(key, desc, require, dict, default)
        # 赋予默认值
        if not require and value is None:
            if isinstance(default, dict):
                return default
            else:
                return dict()

        if not isinstance(value, dict):
            raise ParamsExcept.parameter_dict_error()

        return value


