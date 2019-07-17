import json

class SuccessResult(object):

    def __init__(self, *args, **kwargs):
        """
        Result消息响应模块
        :param kwargs:
        """
        if len(args) == 1 and (isinstance(args[0], dict) or isinstance(args[0], list)):
            self.content = args[0]
        else:
            self.content = kwargs

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            "data": self.content,
        }

    def dumps(self):
        return json.dumps(self.to_dict())
