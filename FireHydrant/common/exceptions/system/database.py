
from common.exceptions.base import FireHydrantExceptBase

class DatabaseException(FireHydrantExceptBase):

    MAJOR_HTTP_CODE = 591.2

    @classmethod
    def delete_error(cls):
        return cls("删除失败，所有关联事务已回滚")




