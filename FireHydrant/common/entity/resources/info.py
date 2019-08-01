from ...core.dao.proptype import PropType
from ...core.dao.entityBase import EntityBase

class ResourcesInfoEntity(EntityBase):

    def __init__(self, **kwargs):

        # 资源名称
        self.name = PropType.str(default='')
        # 资源大小
        self.size = PropType.float(default=0)
        # 资源hash
        self.hash = PropType.str(default='')

        # 解析参数
        super(ResourcesInfoEntity, self).__init__(**kwargs)