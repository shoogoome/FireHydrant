# -*- coding: utf-8 -*-
# coding:utf-8

import uuid
import time
import hmac
import hashlib

"""
一个密码生成验证模块
"""

KEY = "ACCOUNT_PASSWORD"

def session_signature(msg):
    """
    会话签名
    :param msg:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(str(msg).encode('utf-8'))
    return md5.hexdigest()


def gen_salt():
    """
    盐生成器
    :return:
    """
    msg = '{0}:{1}'.format(
        str(time.time()),
        uuid.uuid4()
    )
    h = hmac.new(
        KEY.encode('utf-8'),
        msg.encode('utf-8'),
        hashlib.md5
    )
    return h.hexdigest().upper()

def password_signature(pwd, salt=KEY):
    """
    密文生成器
    :param pwd:
    :param salt:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    msg = md5.hexdigest()

    h = hmac.new(
        salt.encode('utf-8'),
        msg.encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()

def __parse_password_hmac(pwd):
    """
    解析密文
    :param pwd:
    :return:
    """
    struct = pwd.split(';')
    if len(struct) > 1:
        p = struct[0]
        salt = struct[1]
        return p, salt
    else:
        return pwd, KEY

def compare_password(source, target):
    """
    密文比较
    :param source: 源明文密码
    :param target: 目标密文
    :return:
    """
    target_pwd, salt= __parse_password_hmac(target)
    signed = password_signature(source, salt)

    return signed == target_pwd


def build_password_signature(pwd, salt):
    """
    构建新标准的密文格式
    :param pwd: 密码原文
    :param salt: 盐
    :return:
    """
    return '{0};{1}'.format(
        password_signature(pwd, salt),
        salt,
    )