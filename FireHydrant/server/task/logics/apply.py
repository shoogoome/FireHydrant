
from ..models import TaskApply
from common.exceptions.task.apply import TaskInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class TaskApplyLogic(object):

    NORMAL_FIELD = [
        'task', 'task__id', 'task__title', 'author', 'author__id',
        'content', 'exhibition', 'exhibition__id', 'create_time',
        'update_time'
    ]

    def __init__(self, auth, aid):
        """
        任务申请
        :param auth:
        :param aid:
        """
        self.auth = auth

        if isinstance(aid, TaskApply):
            self.apply = aid
        else:
            self.apply = self.get_apply_model(aid)

    def get_apply_model(self, aid):
        """
        获取申请表model
        :param aid:
        :return:
        """
        if aid is None or aid == '':
            return

        apply = TaskApply.objects.get_once(pk=aid)
        if apply is None:
            raise TaskInfoExcept.apply_is_not_exists()

        return apply

    def get_apply_info(self):
        """
        获取申请表信息
        :return:
        """
        return model_to_dict(self.apply, self.NORMAL_FIELD)





