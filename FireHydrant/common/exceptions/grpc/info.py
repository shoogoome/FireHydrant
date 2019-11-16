from common.exceptions.base import FireHydrantExceptBase

class FireHydrantFaceUGrpcExcept(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 591.3

    @classmethod
    def server_except(cls):
        return cls("服务端异常")



