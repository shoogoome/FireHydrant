from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class FaceURecordEntity(EntityBase):

    def __init__(self, **kwargs):

        # 识别图片存储列表
        self.storage = PropType.list(default=[])

        # 结果信息
        self.record = PropType.list(default=[])

        # 解析参数
        super(FaceURecordEntity, self).__init__(**kwargs)