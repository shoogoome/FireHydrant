
from ..models import Task
from common.exceptions.task.task import TaskInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class TaskLogic(object):

    NORMAL_FIELD = [
        'author', 'author__id', 'author__nickname', 'title', 'content',
        'task_type', 'stage', 'classification', 'commission', 'config',
        'create_time', 'update_time', 'resource_links'
    ]

    def __init__(self, auth, tid=''):
        """
        INIT
        :param auth:
        :param tid:
        """
        self.auth = auth

        if isinstance(tid, Task):
            self.task = tid
        else:
            self.task = self.get_task_model(tid)

    def get_task_model(self, tid):
        """
        获取任务model
        :param tid:
        :return:
        """
        if tid is None or tid == '':
            return None

        task = Task.objects.get_once(pk=tid)
        if task is None:
            raise TaskInfoExcept.task_is_not_exists()
        return task

    def get_task_info(self):
        """
        获取任务信息
        :return:
        """
        info = model_to_dict(self.task, self.NORMAL_FIELD)
        if 'resource_links' in info and 'hash' in info['resource_links']:
            del info['resource_links']['hash']
        return info

