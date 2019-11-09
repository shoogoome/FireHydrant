from django.db import transaction
from ..models import *
from django.db import connection
from common.exceptions.system.database import DatabaseException


def delete_group(group):
    """
    安全删除分组
    级联：分组识别记录，分组成员关联
    :return:
    """
    assert isinstance(group, FaceUGroups), 'Param `account` Type Error'

    with transaction.atomic():
        save_id = transaction.savepoint()
        try:
            gid = group.id
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM `faceU_faceudistinguishrecord` WHERE group_id={0}'.format(gid))
                cursor.execute('DELETE FROM `faceU_faceufacialmakeupmapping` WHERE group_id={0}'.format(gid))
            # 删除本体
            group.delete()
        except Exception as ex:
            transaction.savepoint_rollback(save_id)
            raise DatabaseException.delete_error()
        transaction.savepoint_commit(save_id)

    return True

