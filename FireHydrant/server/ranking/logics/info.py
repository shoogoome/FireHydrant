from django.db import connection

from common.exceptions.ranking.info import RankingInfoExcept
from .factory import RankingRedisClusterFactory


class RankingLogic(object):

    @staticmethod
    def get_task_ranking(task_type=0, ranking_type=0):
        """
        获取任务排行信息
        redis key格式: task:任务类型:榜单类型
        :param task_type:
        :param ranking_type:
        :return:
        """
        redis = RankingRedisClusterFactory()

        key = 'task:{}:{}'.format(task_type, ranking_type)
        if redis.exists(key):
            return redis.get_json(key)

        if not isinstance(task_type, int):
            try:
                task_type = int(task_type)
            except:
                raise RankingInfoExcept.task_type_error()

        with connection.cursor() as cursor:
            cursor.execute("SELECT task.author_id, SUM(task.commission) AS money, account.nickname "
                           "FROM `task_task` AS task, `account_account` AS account "
                           "WHERE account.id = task.author_id AND stage = 4 AND task_type = %s "
                           "GROUP BY author_id "
                           "ORDER BY money DESC LIMIT 50", [task_type])
            row = cursor.fetchall()

        data = [{
            'id': i[0],
            'money': i[1],
            'nickname': i[2]
        } for i in row]

        redis.set_json(key, data)
        return data


