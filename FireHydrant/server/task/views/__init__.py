from .classification.info import TaskClassificationInfoView
from .classification.list import TaskClassificationListView
from .info import TaskInfoView
from .list import TaskListView
from .apply import TaskApplyInfoView, TaskApplyManageView
from .report import TaskReportView

__all__ = [
    # 任务分类
    'TaskClassificationInfoView', 'TaskClassificationListView',
    # 任务信息
    'TaskInfoView', 'TaskListView',
    # 任务申请
    'TaskApplyInfoView', 'TaskApplyManageView',
    # 任务汇报
    'TaskReportView',
]