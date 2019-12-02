import base64
import hashlib
import json
import time

from server.faceU.models import FaceUAccount
from .authModel import FireHydrantAuthorization
from ..dao.redis import RedisClusterFactory
from ...constants import params


class FireHydrantClientAuthorization(FireHydrantAuthorization):
    """
    客户端授权
    """

    def __init__(self, request, view):
        """
        auth验证
        :param request:
        :param view:
        """
        super(FireHydrantClientAuthorization, self).__init__(request=request, view=view)
        self.request = request
        self.view = view
        self.__redis = RedisClusterFactory("client:session", params.SESSION_EFFECTIVE_TIME)
        self.__effective_time = params.SESSION_EFFECTIVE_TIME

        self.auth_by_token()

    def auth_by_token(self):
        """
        token载入登陆信息
        :return:
        """
        token = self.request.META.get("HTTP_FIRE_AUTH_TOKEN", "")
        token_key = "{0}@{1}".format(self.__effective_time, token)
        token_info = self.__redis.get(token_key)
        try:
            if not token_info:
                return False
            token_info = base64.b64decode(token_info).decode('utf-8')
            token_info = json.loads(token_info)
            effective_time = float(token_info.get('effective_time', 0))
            if time.time() > effective_time:
                self.__redis.delete(token_key)
                return False

            account_id = token_info.get('account_id', '')
            if self.set_login_status(account_id):
                return True
            else:
                self.__redis.delete(token_key)
            return False
        except:
            return False

    def create_token(self):
        """
        创建登陆token
        :return:
        """
        md5 = hashlib.md5()
        md5.update(str(time.time()).encode('utf-8'))
        token = md5.hexdigest()

        token_key = "{0}@{1}".format(self.__effective_time, token)
        effective_time = time.time() + self.__effective_time
        token_info = {
            "account_id": self._account.id,
            "effective_time": effective_time,
        }
        msg = base64.b64encode(json.dumps(token_info).encode('utf-8')).decode('utf-8')
        # session信息
        self.__redis.set(token_key, msg)

        return token

    @staticmethod
    def fetch_account_by_id(aid):
        """
        id查询账户model
        :param aid:
        :return:
        """
        return FaceUAccount.objects.get_once(pk=aid)

    def set_login_status(self, account_id):
        """
        挂起用户信息
        :param account_id:
        :return:
        """
        if account_id is not None:
            account = FireHydrantClientAuthorization.fetch_account_by_id(account_id)
            if account is not None:
                self._is_login = True
                self._account = account
                return True

        return False
