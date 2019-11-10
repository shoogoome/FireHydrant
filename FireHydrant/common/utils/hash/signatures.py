# -*- coding: utf-8 -*-
# coding:utf-8

import base64
import hashlib
import hmac
import json
import time
import uuid

from FireHydrant.settings import HMAC_SALT, ACCOUNT_PASSWORD_SALT
from common.constants.params import COOKIE_EFFECTIVE_TIME

"""
一个密码生成验证模块
"""


def session_signature(msg):
    """
    会话签名
    :param msg:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(str(msg).encode('utf-8'))
    return md5.hexdigest()


def cookie_signature(msg):
    """
    cookie
    :param msg:
    :return:
    """
    key = "%s@%s" % (ACCOUNT_PASSWORD_SALT, HMAC_SALT)
    h = hmac.new(
        key.encode('utf-8'),
        str(msg).encode('utf-8'),
        hashlib.sha256
    )
    return h.hexdigest()


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
        ACCOUNT_PASSWORD_SALT.encode('utf-8'),
        msg.encode('utf-8'),
        hashlib.md5
    )
    return h.hexdigest().upper()


def password_signature(pwd, salt=ACCOUNT_PASSWORD_SALT):
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
        return pwd, ACCOUNT_PASSWORD_SALT


def compare_password(source, target):
    """
    密文比较
    :param source: 源明文密码
    :param target: 目标密文
    :return:
    """
    target_pwd, salt = __parse_password_hmac(target)
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


def generate_token(payload, expire=COOKIE_EFFECTIVE_TIME):
    """
    生成下载密钥
    :param payload:
    :param expire:
    :return:
    """
    if not payload:
        return ""

    payload_str = json.dumps(payload)
    token = cookie_signature(payload_str)
    payload_encode = base64.b64encode(payload_str.encode("utf-8")).decode()

    return "{}.{}".format(payload_encode, token)
