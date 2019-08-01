from ..models import TaskClassification
from common.exceptions.task.classification import TaskClassificationExcept
from common.utils.helper.m_t_d import model_to_dict
from .factory import ClassificationRedisClusterFactory
from django.db.models import QuerySet

class TaskClassificationLogic(object):

    NORMAL_FILE = [
        'id', 'name', 'description',
    ]

    def __init__(self, auth, cid):
        """
        INIT
        :param auth:
        :param cid:
        """
        self.redis = None

        if isinstance(cid, TaskClassification):
            self.classification = cid
        else:
            self.classification = self.get_classification_model(cid)

    def get_classification_model(self, cid):
        """
        获取分类
        :param cid:
        :return:
        """
        if cid == '' or cid is None:
            return None

        classification = TaskClassification.objects.get_once(pk=cid)
        if classification is None:
            raise TaskClassificationExcept.classification_is_not_exists()
        return classification

    def get_classification_info(self):
        """
        获取分类信息
        :return:
        """
        if self.redis is None: self.redis = ClassificationRedisClusterFactory()
        if self.redis.exists(str(self.classification.id)):
            return self.redis.get_json(str(self.classification.id))

        info = model_to_dict(self.classification, self.NORMAL_FILE)
        info['children'] = [{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in TaskClassification.objects.filter(parent_id=info.get('id', -1))]

        self.redis.set_json(str(self.classification.id), info)
        return info

    @staticmethod
    def get_all_classification_info() -> list:
        """
        获取所有分类信息
        :return:
        """
        redis = ClassificationRedisClusterFactory()
        if redis.exists('all'):
            return redis.get_json('all')

        classifications = TaskClassification.objects.all()
        root_classification = classifications.filter(parent__isnull=True)
        data = TaskClassificationLogic.recursion_get_info(root_classification, classifications)

        redis.set_json('all', data)
        return data

    @staticmethod
    def recursion_get_info(children_classifications: QuerySet, classifications: QuerySet) -> list:
        """
        组建分类树
        :param children_classifications: 同父节点的节点群
        :param classifications: 全部节点
        :return: 构建后的list
        """
        data = list()
        for root in children_classifications:
            try:
                info = {
                    'id': root.id,
                    'name': root.name,
                    'description': root.description
                }
                root_children_classifications = classifications.filter(parent=root)
                children = TaskClassificationLogic.recursion_get_info(root_children_classifications, classifications)
                if len(children) > 0:
                    info['children'] = children
                data.append(info)
            except:
                pass
        return data