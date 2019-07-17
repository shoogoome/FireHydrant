from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class TaskImplementEntity(EntityBase):

    def __init__(self, **kwargs):

        # 阶段开始时间
        self.stage_start_time = PropType.float(default=0)

        # 阶段结束时间
        self.stage_end_time = PropType.float(default=0)

        # 阶段任务标题
        self.title = PropType.str(default='')

        # 任务描述
        self.describe = PropType.str(default='')

        # 解析参数
        super(TaskImplementEntity, self).__init__(**kwargs)