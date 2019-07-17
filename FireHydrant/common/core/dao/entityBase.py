import json
from .proptype import PropType

class EntityBase(object):
    """
    entityBase
    """

    EntityBaseFun = ['update', 'dump', 'parse', 'dumps']

    def __init__(self, **kwargs):
        """
        INIT
        """
        success_key = self.update(kwargs)

        for key, val in self.__dict__.items():
            if key in self.EntityBaseFun or key in success_key:
                continue

            # 初始化未赋值的PropType类定义
            prop_type = object.__getattribute__(self, key)
            if isinstance(prop_type, PropType):
                self.__setattr__(key, prop_type())

    def update(self, source):
        """
        参数写入类中
        :param source:
        :return:
        """
        success_keys = []
        self_keys = self.__dict__.keys()
        for key, val in source.items():
            if key not in self_keys:
                continue
            item = self.__getattribute__(key)
            if item is None: continue
            if isinstance(item, PropType):
                self.__setattr__(key, self.__parse(key, val, item))
            else:
                self.__setattr__(key, val)
            success_keys.append(key)
        return success_keys

    def __parse(self, key, val, prop_type):
        """
        解析ProPType类
        :param key:
        :param val:
        :param prop_type:
        :return:
        """
        type_class = prop_type.get_type()
        if type_class == list:
            if isinstance(val, list):
                tmp = []
                entity = prop_type.get_entity_require()
                if isinstance(entity, PropType):
                    for item in val:
                        tmp.append(self.__parse(item, key, entity))
                elif issubclass(entity, EntityBase):
                    for item in val:
                        tmp.append(entity(**item))
                else:
                    for item in val:
                        tmp.append(item)
                return tmp
            elif val is None:
                return []
            else:
                raise AttributeError('[EntityBaseParse] "{0}" not a list.'.format(val))

        elif issubclass(type_class, EntityBase):
            if isinstance(val, dict):
                return type_class(**val)
            else:
                return type_class()
        else:
            return val


    def dump(self):
        """
        解析成员为字典
        :return:
        """
        tmp = {}
        for key, val in self.__dict__.items():
            if key[:2] == '__' or key[:1] == '_' or key in EntityBase.EntityBaseFun:
                continue
            if isinstance(val, PropType):
                tmp[key] = val.get_value()
            else:
                tmp[key] = val
        return tmp

    @classmethod
    def parse(cls, data):
        """
        解析
        :return:
        """
        data = json.loads(data)
        return cls(**data)

    def dumps(self):
        """
        解析成员为字典格式字符串
        :return:
        """
        return json.dumps(self.dump())

    def set_value(self, key, val):
        """
        设置val
        :param key:
        :param val:
        :return:
        """
        item = self.__getattribute__(key)
        if item is None:
            return
        if isinstance(item, PropType):
            item.set_value(val)
            self.__setattr__(key, item)
        else:
            self.__setattr__(key, val)

    def __getattribute__(self, key):
        """
        重写get函数
        :param key:
        :return:
        """
        try:
            return object.__getattribute__(self, key)
        except:
            return None
