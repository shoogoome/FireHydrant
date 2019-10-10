from ..models import PracticeAttendance
from .arrangement import ArrangementLogic
from common.exceptions.practice.attendance.info import PracticeAttendanceInfoExcept
from common.utils.helper.m_t_d import model_to_dict

class AttendanceLogic(ArrangementLogic):

    NORMAL_FIELDS = [
        'school', 'school__id', 'course', 'course__id', 'arrangement',
        'arrangement__id', 'student', 'student__id', 'leaver',
        'absent', 'late', 'create_time', 'update_time'
    ]

    def __init__(self, auth, sid, cid, aid, atid=''):

        super(AttendanceLogic, self).__init__(auth, sid, cid, aid)
        if isinstance(atid, PracticeAttendance):
            self.attendance = atid
        else:
            self.attendance = self.get_attendance_model(atid)

    def get_attendance_model(self, atid):
        """
        获取考勤model
        :param atid:
        :return:
        """
        if not atid:
            return None

        attendance = PracticeAttendance.objects.get_once(atid)
        if not attendance:
            raise PracticeAttendanceInfoExcept.attendance_is_not_exists()
        return attendance

    def get_attendance_info(self):
        """
        获取考勤记录信息
        :return:
        """
        if not self.attendance:
            return {}
        return model_to_dict(self.attendance, self.NORMAL_FIELDS)