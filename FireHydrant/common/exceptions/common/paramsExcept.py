
from common.exceptions.base import FireHydrantExceptBase

class ParamsExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 550.1

    @classmethod
    def parameter_none_error(cls, key):
        return cls("{0}参数不得为空".format(key))

    @classmethod
    def parameter_int_error(cls):
        return cls("不是一个有效的int值")

    @classmethod
    def parameter_float_error(cls):
        return cls("不是一个有效的float值")

    @classmethod
    def parameter_str_error(cls):
        return cls("不是一个有效的str值")

    @classmethod
    def parameter_list_error(cls):
        return cls("不是一个有效的list值")

    @classmethod
    def parameter_dict_error(cls):
        return cls("不是一个有效的dict值")

    @classmethod
    def model_diff_error(cls):
        return cls("不得在diff模式下运行")



