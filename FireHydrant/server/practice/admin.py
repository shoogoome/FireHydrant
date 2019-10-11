from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PracticeStudentUser)
admin.site.register(PracticeCourse)
admin.site.register(PracticeArrangement)
admin.site.register(PracticeClassroom)
admin.site.register(PracticeSchool)
admin.site.register(PracticeTag)
admin.site.register(PracticeClassroomUser)
admin.site.register(PracticeAttendance)
admin.site.register(PracticeEvaluateStudentToCourse)
admin.site.register(PracticeEvaluateTeacherToStudent)
admin.site.register(PracticeEvaluateStudentToTeacher)

