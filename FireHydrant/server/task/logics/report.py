from ..models import TaskClassification
from common.exceptions.task.classification import TaskClassificationExcept
from common.utils.helper.m_t_d import model_to_dict
from .factory import ClassificationRedisClusterFactory
from django.db.models import QuerySet
from ..models import TaskReport
from common.exceptions.task.report import TaskReportExcept
from server.resources.logic.info import ResourceLogic

class TaskReportLogic(object):

    NORMAL_FILE = [
        'id', 'summary', 'create_time', 'update_time'
    ]


    def __init__(self, auth, tid, rid):
        """
        INIT
        :param auth:
        :param tid:
        :param rid:
        """
        self.auth = auth

        if isinstance(rid, TaskReport):
            self.report = rid
        else:
            self.report = self.get_report_model(rid)

    def get_report_model(self, rid):
        """
        获取汇报model
        :param rid:
        :return:
        """
        if not rid or rid == '':
            return None
        report = TaskReport.objects.get_once(pk=rid)
        if not report:
            raise TaskReportExcept.report_is_not_exists()
        return report

    def get_report_info(self):
        """
        获取汇报详情
        :return:
        """
        if self.report is None:
            return {}
        info = model_to_dict(self.report, self.NORMAL_FILE)
        info['resource'] = [{
            'name': i.name,
            'size': i.size,
            'create_time': i.create_time,
            'token': ResourceLogic.get_download_token(i.hash)
        } for i in self.report.resource.all()]

        return info


