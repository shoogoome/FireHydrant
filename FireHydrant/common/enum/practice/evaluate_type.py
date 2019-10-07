# -*- coding: utf-8 -*-
# coding:utf-8

from ...core.dao import EnumBase


class EvaluateTypeEnum(EnumBase):

    STUDENT_TO_COURSE = 0
    STUDENT_TO_TEACHER = 1
    TEACHER_TO_STUDENT = 2

    __default__ = STUDENT_TO_COURSE
    __desc__ = {
        'STUDENT_TO_COURSE': '学生 -> 课程',
        'STUDENT_TO_TEACHER': '学生 -> 老师',
        'TEACHER_TO_STUDENT': '老师 -> 学生',
    }
