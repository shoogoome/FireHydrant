from django.db import models
from common.core.dao.time_stamp import TimeStampField
from common.core.dao.cache.factory import delete_model_single_object_cache
from common.core.dao.cache.model_manager import FireHydrantModelManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.enum.practice.oddeven import OddEvenEnum
from common.enum.practice.attendance_state import AttendanceStateEnum
from .logics.signals import handle_tag_post_save_delete

# Create your models here.

class PracticeSchool(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理学校"
        verbose_name_plural = "爱阅读后台管理学校表"
        app_label = 'practice'


    # 学校名称
    name = models.CharField(max_length=255)

    # 学校logo
    logo = models.CharField(max_length=200, default='', blank=True)

    # 简介
    description = models.TextField(default="")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()


    def __str__(self):
        return '[{}] 学校名称：{}'.format(self.id, self.name)


class PracticeStudentUser(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理学生账户"
        verbose_name_plural = "爱阅读后台管理学生账户表"
        app_label = 'practice'

    # 账号关联
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 学校关联
    school = models.ForeignKey('practice.PracticeSchool', on_delete=models.CASCADE)

    # 学号
    code = models.CharField(max_length=255)

    # 真实名称
    realname = models.CharField(max_length=255)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 学校名称: {}, 真实名称: {}'.format(
            self.id, self.school.name, self.realname
        )


class PracticeTag(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理标签"
        verbose_name_plural = "爱阅读后台管理标签表"
        app_label = 'practice'

    # 名称
    name = models.CharField(max_length=125)

    # 父节点
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()


    def __str__(self):
        return '[{}] 名称: {}'.format(
            self.id, self.name
        )

class PracticeCourse(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理课程"
        verbose_name_plural = "爱阅读后台管理课程表"
        app_label = 'practice'

    # 学校
    school = models.ForeignKey('practice.PracticeSchool', on_delete=models.CASCADE)

    # 创建人
    author = models.ForeignKey('account.Account', on_delete=models.SET_NULL, null=True, blank=True)

    # 标签
    tag = models.ForeignKey('practice.PracticeTag', on_delete=models.SET_NULL, null=True, blank=True)

    # 名称
    name = models.CharField(max_length=125)

    # 简介
    description = models.CharField(max_length=255)

    # 开始时间
    start_time = TimeStampField(default=0)

    # 结束时间
    end_time = TimeStampField(default=0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 名称: {}, 归属学校: {}'.format(
            self.id, self.name, self.school.name
        )


class PracticeArrangement(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理课程排课"
        verbose_name_plural = "爱阅读后台管理课程排课表"
        app_label = 'practice'

    # 课程
    course = models.ForeignKey('practice.PracticeCourse', on_delete=models.CASCADE)

    # 排课名称
    name = models.CharField(max_length=50, blank=True, default="")

    # 周几
    day_of_week = models.PositiveSmallIntegerField(default=0)

    # 开始周
    start_week = models.PositiveSmallIntegerField(default=0)

    # 结束周
    end_week = models.PositiveSmallIntegerField(default=0)

    # 单双周
    odd_even = models.PositiveSmallIntegerField(**OddEvenEnum.get_models_params())

    # 开始节
    start_section = models.PositiveSmallIntegerField(default=0)

    # 结束节
    end_section = models.PositiveSmallIntegerField(default=0)

    # 开始时间(24小时)
    start_time = models.PositiveIntegerField(default=0)

    # 结束时间(24小时)
    end_time = models.PositiveIntegerField(default=0)

    # 学生信息(选课信息)
    students = models.ManyToManyField('practice.PracticeStudentUser', blank=True, related_name='course_arrangement_student')

    # 创建时间（入队时间）
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 关联课程: {}, 排课名称: {}'.format(
            self.id, self.course.name, self.name
        )

class PracticeAttendance(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理课程考勤"
        verbose_name_plural = "爱阅读后台管理课程考勤表"
        app_label = 'practice'

    # 学校
    school = models.ForeignKey('practice.PracticeSchool', on_delete=models.CASCADE)

    # 课程
    course = models.ForeignKey('practice.PracticeCourse', on_delete=models.CASCADE)

    # 排课
    arrangement = models.ForeignKey('practice.PracticeArrangement', on_delete=models.CASCADE)

    # 学生
    student = models.ForeignKey('practice.PracticeStudentUser', on_delete=models.CASCADE)

    # 请假
    leaver = models.IntegerField(default=0)

    # 缺勤
    absent = models.IntegerField(default=0)

    # 迟到
    late = models.IntegerField(default=0)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 学校: {}, 课程: {}, 排课: {}, 学生: {}'.format(
            self.id, self.school_id, self.course_id,
            self.arrangement_id, self.student_id
        )

class PracticeClassroom(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理教室"
        verbose_name_plural = "爱阅读后台管理教室表"
        app_label = 'practice'

    # 学校
    school = models.ForeignKey('practice.PracticeSchool', on_delete=models.CASCADE)

    # 大小
    size = models.IntegerField(default=0)

    # 名称
    name = models.CharField(max_length=125)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 学校: {}, 名称: {}'.format(
            self.id, self.school.name, self.name
        )

class PracticeClassroomUser(models.Model):

    class Meta:
        verbose_name = "爱阅读后台管理教室使用"
        verbose_name_plural = "爱阅读后台管理教室使用表"
        app_label = 'practice'

    # 创建人
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 教室
    classroom = models.ForeignKey('practice.PracticeClassroom', on_delete=models.CASCADE)

    # 排课
    arrangement = models.ForeignKey('practice.PracticeArrangement', on_delete=models.CASCADE)

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()

    def __str__(self):
        return '[{}] 教室: {}, 排课: {}'.format(
            self.id, self.classroom_id, self.arrangement_id
        )

class PracticeEvaluateBase(models.Model):

    class Meta:
        abstract = True

    # 评分
    star = models.PositiveSmallIntegerField(default=0)

    # 评语
    message = models.TextField(default="")

    # 创建时间
    create_time = TimeStampField(auto_now_add=True)

    # 更新时间
    update_time = TimeStampField(auto_now=True)

    # 重构管理器
    objects = FireHydrantModelManager()


class PracticeEvaluateStudentToCourse(PracticeEvaluateBase):

    class Meta:
        verbose_name = "爱阅读后台管理课程学生评价课程"
        verbose_name_plural = "爱阅读后台管理课程学生评价课程表"
        app_label = 'practice'

    # 创建人
    author = models.ForeignKey('practice.PracticeStudentUser', on_delete=models.CASCADE)

    # 课程
    course = models.ForeignKey('practice.PracticeCourse', on_delete=models.CASCADE)

    def __str__(self):
        return '[{}] 学生: {}, 课程: {}'.format(
            self.id, self.author.realname, self.course.name
        )

class PracticeEvaluateStudentToTeacher(PracticeEvaluateBase):
    class Meta:
        verbose_name = "爱阅读后台管理课程学生评价教师"
        verbose_name_plural = "爱阅读后台管理课程学生评价教师表"
        app_label = 'practice'

    # 创建人
    author = models.ForeignKey('practice.PracticeStudentUser', on_delete=models.CASCADE)

    # 教师
    teacher = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    def __str__(self):
        return '[{}] 学生: {}, 老师: {}'.format(
            self.id, self.author.realname, self.teacher.nickname
        )

class PracticeEvaluateTeacherToStudent(PracticeEvaluateBase):
    class Meta:
        verbose_name = "爱阅读后台管理课程教师评价学生"
        verbose_name_plural = "爱阅读后台管理课程教师评价学生表"
        app_label = 'practice'

    # 创建人
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    # 学生
    student = models.ForeignKey('practice.PracticeStudentUser', on_delete=models.CASCADE)

    def __str__(self):
        return '[{}] 老师: {}, 学生: {}'.format(
            self.id, self.author.nickname, self.student.realname
        )


receiver(post_save, sender=PracticeSchool)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeSchool)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeStudentUser)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeStudentUser)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeTag)(handle_tag_post_save_delete)
receiver(post_delete, sender=PracticeTag)(handle_tag_post_save_delete)

receiver(post_save, sender=PracticeCourse)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeCourse)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeArrangement)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeArrangement)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeAttendance)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeAttendance)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeClassroom)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeClassroom)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeClassroomUser)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeClassroomUser)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeEvaluateBase)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeEvaluateBase)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeEvaluateTeacherToStudent)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeEvaluateTeacherToStudent)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeEvaluateStudentToTeacher)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeEvaluateStudentToTeacher)(delete_model_single_object_cache)

receiver(post_save, sender=PracticeEvaluateStudentToCourse)(delete_model_single_object_cache)
receiver(post_delete, sender=PracticeEvaluateStudentToCourse)(delete_model_single_object_cache)



