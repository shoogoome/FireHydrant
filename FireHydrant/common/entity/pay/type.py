from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class PayTypeEntity(EntityBase):

    def __init__(self, **kwargs):

        # 支付宝账号(用户系统向用户转账)
        self.alipay = PropType.str(default='')

        # 此后在陆续接入其他方支付商

        # 解析参数
        super(PayTypeEntity, self).__init__(**kwargs)