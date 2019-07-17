from enum import Enum


class EnumBase(Enum):

    @classmethod
    def get_default_value(cls):
        """
        获取默认enum值
        :return:
        """
        if hasattr(cls, '__dafault__'):
            return cls.__dafault__

        items = list(cls.__members__.items())
        if len(items) > 0:
            name, item = items[0]
            return item.value
        else:
            raise AttributeError("Enum Error!")

    @classmethod
    def get_choices(cls, with_desc=True):
        """
        Enum转换DjangoModel的choose选项需要的数据结构
        :param with_desc: 是否显示枚举项目的描述
        :return: [(0, 'xxxx'), (1, 'yyyy') ...]
        :param with_desc:
        :return:
        """
        res = []
        for name, item in cls.__members__.items():
            if with_desc:
                res.append((item.value, item.get_desc()))
            else:
                res.append((item.value, name))

        return res

    def get_desc(self):
        """
        获取enum值
        :return:
        """
        if hasattr(self, 'name'):
            return self.__desc__.get(self.name, self.name)
        return self.name

    @classmethod
    def get_models_params(cls):
        """
        自动构建DjangoModel参数选项
        :return:
        """
        return {
            "default": cls.get_default_value(),
            "choices": cls.get_choices()
        }

    def __int__(self):
        return self.value
