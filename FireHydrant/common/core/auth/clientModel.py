# from .authModel import FireHydrantAuthorization
# import base64
# import hashlib
# import json
# import time
#
from .authModel import FireHydrantAuthorization
# from ..dao.redis import RedisClusterFactory
# from ...constants import params
#
#
class FireHydrantClientAuthorization(FireHydrantAuthorization):
    ...
#     """
#     客户端授权
#     """
#
#     def __init__(self, request, view):
#         """
#         auth验证
#         :param request:
#         :param view:
#         """
#         super(FireHydrantClientAuthorization, self).__init__(request=request, view=view)
#         self.request = request
#         self.view = view
#         self.__redis = RedisClusterFactory("Session", params.SESSION_EFFECTIVE_TIME)
#         self.__effective_time = params.SESSION_EFFECTIVE_TIME
#         # self.__school_time = params.SCHOOL_ID_SESSION_EFFECTIVE_TIME_TIME
#
#         self.auth_by_token()
#
#     def auth_by_token(self):
#         """
#         token载入登陆信息
#         :return:
#         """
#         token = self.request.META.get("HTTP_HOHO_AUTH_TOKEN", "")
#         token_key = "{0}@{1}".format(self.__effective_time, token)
#         token_info = self.__redis.get(token_key)
#         try:
#             if token_info is None:
#                 return False
#             token_info = base64.b64decode(token_info).decode('utf-8')
#             token_info = json.loads(token_info)
#             effective_time = float(token_info.get('effective_time', 0))
#             if time.time() > effective_time:
#                 self.__redis.delete(token_key)
#                 return False
#
#             account_id = token_info.get('account_id', '')
#             if self.set_login_status(account_id):
#                 self._school_id = self.__redis.get("{}@{}".format(self.__school_time, account_id))
#                 return True
#             else:
#                 self.__redis.delete(token_key)
#             return False
#         except:
#             return False
#
#     def update_school_id(self, aid):
#         """
#         更新当前学校id
#         :param aid:
#         :return:
#         """
#         aid = str(aid)
#         school_id_key = "{}@{}".format(self.__school_time, self._account.id)
#         self.__redis.set(school_id_key, aid, self.__school_time)
#
#     def create_token(self):
#         """
#         创建登陆token
#         :return:
#         """
#         md5 = hashlib.md5()
#         md5.update(str(time.time()).encode('utf-8'))
#         token = md5.hexdigest()
#
#         token_key = "{0}@{1}".format(self.__effective_time, token)
#         effective_time = time.time() + self.__effective_time
#         token_info = {
#             "account_id": self._account.id,
#             "effective_time": effective_time,
#         }
#         msg = base64.b64encode(json.dumps(token_info).encode('utf-8')).decode('utf-8')
#         # session信息
#         self.__redis.set(token_key, msg)
#         # 当前学校id
#         school_id_key = "{}@{}".format(self.__school_time, self._account.id)
#         if not self.__redis.exists(school_id_key):
#             self.__redis.set(school_id_key, "", self.__school_time)
#
#         return token
