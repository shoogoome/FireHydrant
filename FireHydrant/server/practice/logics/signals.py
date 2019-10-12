from common.core.dao.cache.factory import delete_model_single_object_cache
from server.task.logics.factory import ClassificationRedisClusterFactory
from common.enum.task.stage import TaskStageEnum
from server.ranking.logics.factory import RankingRedisClusterFactory
from common.enum.ranking.type import RankingTypeEnum
from .factory import TagRedisClusterFactory

def handle_tag_post_save_delete(instance, **kwargs):
    # 清除数据库缓存
    delete_model_single_object_cache(instance, **kwargs)

    # 分类变动则删除缓存
    factory = TagRedisClusterFactory()
    try:
        factory.delete("all")
    except:
        pass



