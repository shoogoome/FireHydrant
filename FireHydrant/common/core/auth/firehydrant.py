from server.account.models import Account
from common.constants.params import *
from common.utils.hash.signatures import session_signature, cookie_signature
import base64
from .redis_cookie import RedisSessionFactory
import time
import json
from .authModel import FireHydrantAuthorization

class FireHydrantAuthAuthorization(FireHydrantAuthorization):

    def __init__(self, request, view):
        """
        auth验证
        :param request:
        :param view:
        """
        super(FireHydrantAuthAuthorization, self).__init__(request=request, view=view)
        self.request = request
        self.view = view
        self.load_from_session()

    def load_from_session(self):
        """
        载入登陆信息
        :return:
        """
        # 读取用户id
        account_id = self.request.session.get(FIREAUTHSESSION, '')
        # 挂起登陆信息
        if not self.set_login_status(account_id):
            self.load_from_cookie()

    def load_from_cookie(self):
        """
        从Cookie里读取登录信息
        :return:
        """
        user_token = self.request.COOKIES.get(FIREAUTHSIGN, '')
        # 取不到cookie
        if user_token.strip() == '':
            return False

        user_token = user_token.split('.')
        # 格式错误
        if len(user_token) != 2:
            return False

        payload_str = base64.b64decode(user_token[0]).decode()
        # 签名验证
        if cookie_signature(payload_str) != user_token[1]:
            return False

        payload = json.loads(payload_str)
        if int(time.time()) >= payload.get('expire_at', -1):
            return False
        account_id = payload.get('account_id', -1)
        return self.set_login_status(account_id)

    def set_session(self):
        """
        设置登陆信息
        :return:
        """
        if self._account is None:
            self.request.session[FIREAUTHSESSION] = ""
            self.set_cookie("")
            return False

        self.request.session[FIREAUTHSESSION] = self._account.id
        # 产生登陆签名
        self.set_cookie(self._account.id)
        return True

    def set_cookie(self, aid, expire=COOKIE_EFFECTIVE_TIME):
        """
        设置cookie
        :return:
        """
        payload = {
            "expire_at": int(time.time() + expire),
            "account_id": aid
        }
        payload_str = json.dumps(payload)
        token = cookie_signature(payload_str)
        payload_encode = base64.b64encode(payload_str.encode("utf-8")).decode()

        self.view.set_cookie(
            key=FIREAUTHSIGN,
            value='{}.{}'.format(payload_encode, token)
        )
