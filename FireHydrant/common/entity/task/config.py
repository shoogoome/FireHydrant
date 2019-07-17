from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase
from .implement import TaskImplementEntity

class TaskConfigEntity(EntityBase):

    def __init__(self, **kwargs):

        # 发布时间
        self.publish_start_time = PropType.float(default=0)

        # 最迟确认时间
        self.publish_end_time = PropType.float(default=0)

        # 执行阶段
        self.implement = PropType.dict(default={
            "staged": 0,
            "stage": TaskImplementEntity().dump()
        })

        # 解析参数
        super(TaskConfigEntity, self).__init__(**kwargs)