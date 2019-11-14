from .accounts.login import FaceUAccountLogin, FireHydrantDevelopLogin
from .accounts.logout import FaceUAccountLogout
from .accounts.info import FaceUAccountInfoView
from .accounts.list_mget import FaceUAccountListMget
from .groups.info import FaceUGroupInfo
from .groups.list_mget import FaceUGroupListMget
from .groups.manage import FaceUGroupManageView, FaceUGroupManageMany
from .distinguish.distinguish import FaceUDistinguishView
from .record.info import FaceURecordInfoView
__all__ = [
    # 账户
    'FaceUAccountLogin', 'FireHydrantDevelopLogin', 'FaceUAccountInfoView',
    'FaceUAccountListMget', 'FaceUAccountLogout',
    # 分组
    'FaceUGroupInfo', 'FaceUGroupListMget', 'FaceUGroupManageView', 'FaceUGroupManageMany',
    # 识别
    'FaceUDistinguishView',
    # 记录
    'FaceURecordInfoView',
]