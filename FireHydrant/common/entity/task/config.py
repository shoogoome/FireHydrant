from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase
from .implement import TaskImplementEntity

class TaskConfigEntity(EntityBase):

    def __init__(self, **kwargs):

        # 最迟确认时间
        self.publish_end_time = PropType.float(default=0.0)

        # 开发时长
        self.development_time = PropType.float(default=0.0)

        # 委托金
        self.commission = PropType.float(default=0.0)

        # 解析参数
        super(TaskConfigEntity, self).__init__(**kwargs)