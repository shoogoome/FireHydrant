from .school.info.info import PracticeSchoolInfoView
from .school.info.list_mget import PracticeSchoolListMgetView
from .school.student.info import PracticeStudentInfoView
from .school.student.list_mget import PracticeStudentListMgetView
from .course.info.info import PracticeCourseInfoView
from .course.info.list_mget import PracticeCourseListMgetView
from .course.arrangement.info import PracticeArrangementInfoView
from .course.arrangement.list_mget import PracticeArrangementListMgetView
from .course.arrangement.student import PracticeArrangementStudentInfoView
from .attendance.info import PracticeAttendanceInfoView
from .attendance.list_mget import PracticeAttendanceListMgetView
from .tag.info import PracticeTagView
from .tag.list_mget import PracticeTagListView
from .classroom.info import PracticeClassroomInfoView
from .classroom.list_mget import PracticeClassroomListMgetView
from .classroom.classroom_user import PracticeClassroomUserInfoView
from .evaluate.student_course import PracticeStudentToCourseInfoView, PracticeStudentToCourseListMgetView
from .evaluate.student_teacher import PracticeStudentToTeacherInfoView, PracticeStudentToTeacherListMgetView
from .evaluate.teacher_student import PracticeTeacherToStudentInfoView, PracticeTeacherToStudentListMgetView

__all__ = [
    # 学校
    'PracticeSchoolInfoView', 'PracticeSchoolListMgetView',
    # 学生
    'PracticeStudentInfoView', 'PracticeStudentListMgetView',
    # 课程
    'PracticeCourseListMgetView', 'PracticeCourseInfoView',
    # 排课
    'PracticeArrangementInfoView', 'PracticeArrangementListMgetView',
    'PracticeArrangementStudentInfoView',
    # 考勤
    'PracticeAttendanceInfoView', 'PracticeAttendanceListMgetView',
    # 标签
    'PracticeTagView', 'PracticeTagListView',
    # 教室
    'PracticeClassroomInfoView', 'PracticeClassroomListMgetView', 'PracticeClassroomUserInfoView',
    # 评价
    'PracticeStudentToCourseInfoView', 'PracticeStudentToCourseListMgetView',
    'PracticeStudentToTeacherInfoView', 'PracticeStudentToTeacherListMgetView',
    'PracticeTeacherToStudentInfoView', 'PracticeTeacherToStudentListMgetView',
]