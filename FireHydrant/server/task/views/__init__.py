from .classification.info import TaskClassificationInfoView
from .classification.list import TaskClassificationListView
from .info import TaskInfoView
from .list import TaskListView

__all__ = [
    # 任务分类
    'TaskClassificationInfoView', 'TaskClassificationListView',
    # 任务信息
    'TaskInfoView', 'TaskListView'
]