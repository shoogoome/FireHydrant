class PropType(object):
    """
    entity数据类型
    """

    def __init__(self, type_class, **kwargs):
        """
        INIT
        :param kwargs:
        """
        self._type_calss = type_class
        self._value = kwargs.get('default', None)
        self._is_required = kwargs.get('required', False)

    def __call__(self, *args, **kwargs):
        return self._value

    def get_type(self):
        return self._type_calss

    def is_required(self):
        return self.is_required()

    def get_value(self):
        return self._value

    def set_value(self, value):
        if isinstance(value, self._type_calss):
            self._value = value

    def set_required(self, required):
        if isinstance(required, bool):
            self._is_required = required

    def get_entity_required(self):
        return object

    @classmethod
    def int(cls, default=0, required=True):
        return cls(int, default=default, required=required)

    @classmethod
    def float(cls, default=0.0, required=True):
        return cls(float, default=default, required=required)

    @classmethod
    def str(cls, default='', required=True):
        return cls(str, default=default, required=required)

    @classmethod
    def bool(cls, default=False, required=True):
        return cls(bool, default=default, required=required)

    @classmethod
    def list(cls, default=list(), required=True):
        return cls(list, default=default, required=required)

    @classmethod
    def dict(cls, default=dict(), required=True):
        return cls(dict, default=default, required=required)

