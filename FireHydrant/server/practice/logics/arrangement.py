from ..models import PracticeArrangement
from ..logics.course import CourseLogic
from common.exceptions.practice.course.arrangement import PracticeArrangementInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class ArrangementLogic(CourseLogic):

    NORMAL_FIELDS = [
        'course', 'course__id', 'course__name',
        'name', 'day_of_week', 'start_week', 'end_week',
        'odd_even', 'start_section', 'end_section', 'start_time',
        'end_time', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid, cid, aid=''):
        """
        INIT
        :param auth:
        :param sid:
        :param cid:
        :param aid:
        """
        super(ArrangementLogic, self).__init__(auth, sid, cid)
        if isinstance(aid, PracticeArrangement):
            self.arrangement = aid
        else:
            self.arrangement = self.get_arrangement_model(aid)

    def get_arrangement_model(self, aid):
        """
        获取排课model
        :param aid:
        :return:
        """
        if not aid:
            return None
        arrangement = PracticeArrangement.objects.get_once(aid)
        if not arrangement or arrangement.course != self.course:
            raise PracticeArrangementInfoExcept.arrangement_is_not_exists()

        return arrangement

    def get_arrangement_info(self):
        """
        获取排课信息
        :return:
        """
        if self.arrangement is None:
            return {}
        return model_to_dict(self.arrangement, self.NORMAL_FIELDS)
