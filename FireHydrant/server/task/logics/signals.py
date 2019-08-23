from common.core.dao.cache.factory import delete_model_single_object_cache
from server.task.logics.factory import ClassificationRedisClusterFactory
from common.enum.task.stage import TaskStageEnum
from server.ranking.logics.factory import RankingRedisClusterFactory
from common.enum.ranking.type import RankingTypeEnum

def handle_classification_post_save_delete(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 分类变动则删除缓存
    if not kwargs.get('create', False):
        redis = ClassificationRedisClusterFactory()
        if redis.exists(str(instance.id)):
            redis.delete(str(instance.id))
        if redis.exists('all'):
            redis.delete('all')

def handle_task_post_save(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 完成任务则清空排行版缓存
    if not kwargs.get('create', False):
        if instance.stage == int(TaskStageEnum.COMPLETE):
            redis_ranking = RankingRedisClusterFactory()
            try:
                [redis_ranking.delete('task:{}:{}'.format(int(instance.task_type), int(i))) for i in
                 RankingTypeEnum.get_enums_list()]
            except:
                pass

def handle_task_post_delete(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)
    # 清除排行版缓存
    if instance.stage == int(TaskStageEnum.COMPLETE):
        redis_ranking = RankingRedisClusterFactory()
        try:
            [redis_ranking.delete('task:{}:{}'.format(int(instance.task_type), int(i))) for i in
             RankingTypeEnum.get_enums_list()]
        except:
            pass