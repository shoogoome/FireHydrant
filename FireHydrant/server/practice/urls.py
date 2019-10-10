from django.urls import path, include
from .views import *

tag_urlpatterns = [
    path('', PracticeTagView.as_view(method=['POST'])),
    path('/list', PracticeTagListView.as_view(method=['GET'])),
    path('/<int:tid>', PracticeTagView.as_view(method=['GET', 'PUT', 'DELETE'])),
]

school_urlpatterns = [
    path('', PracticeSchoolInfoView.as_view(method=['POST'])),
    path('/list', PracticeSchoolListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeSchoolListMgetView.as_view(method=['POST'])),
    path('/<int:sid>', PracticeSchoolInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
]

classroom_urlpatterns = [
    path('', PracticeClassroomInfoView.as_view(method=['POST'])),
    path('/list', PracticeClassroomListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeClassroomListMgetView.as_view(method=['POST'])),
    path('/<int:cid>', PracticeClassroomInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:cid>/user', PracticeClassroomUserInfoView.as_view(method=['GET', 'POST'])),
    path('/<int:cid>/user/<int:uid>', PracticeClassroomUserInfoView.as_view(method=['DELETE'])),
]

student_urlpatterns = [
    path('', PracticeStudentInfoView.as_view(method=['POST'])),
    path('/list', PracticeStudentListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeStudentListMgetView.as_view(method=['POST'])),
    path('/<int:stid>', PracticeStudentInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
]

course_urlpatterns = [
    path('', PracticeCourseInfoView.as_view(method=['POST'])),
    path('/list', PracticeCourseListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeCourseListMgetView.as_view(method=['POST'])),
    path('/<int:cid>', PracticeCourseInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
]

arrangement_urlpatterns = [
    path('', PracticeArrangementInfoView.as_view(method=['POST'])),
    path('/list', PracticeArrangementListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeArrangementListMgetView.as_view(method=['POST'])),
    path('/<int:aid>', PracticeArrangementInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
    path('/<int:aid>/students', PracticeArrangementStudentInfoView.as_view(method=['GET', 'POST', 'DELETE'])),
]

attendance_urlpatterns = [
    path('', PracticeAttendanceInfoView.as_view(method=['post'])),
    path('/list', PracticeAttendanceListMgetView.as_view(method=['GET'])),
    path('/_mget', PracticeAttendanceListMgetView.as_view(method=['POST'])),
    path('/<int:atid>', PracticeAttendanceInfoView.as_view(method=['GET', 'PUT', 'DELETE'])),
]

urlpatterns = [
    # 标签
    path('/tags', include(tag_urlpatterns)),
    # 学校
    path('/schools', include(school_urlpatterns)),
    # 教室
    path('/schools/<int:sid>/classrooms', include(classroom_urlpatterns)),
    # 学生
    path('/schools/<int:sid>/students', include(student_urlpatterns)),
    # 课程
    path('/schools/<int:sid>/courses', include(course_urlpatterns)),
    # 排课
    path('/schools/<int:sid>/courses/<int:cid>/arrangements', include(arrangement_urlpatterns)),
    # 考勤
    path('/schools/<int:sid>/courses/<int:cid>/arrangements/<int:aid>/attendance', include(attendance_urlpatterns))
]