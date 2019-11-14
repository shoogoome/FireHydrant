from django.db import connection


class FaceUDistinguishLogic(object):

    def __init__(self, auth, group=0):
        """
        人脸识别逻辑
        :param auth:
        :param group:
        """
        self.auth = auth
        self._group = group
        self._overall_situation = True if not group else False

    def to_face_uuid(self):
        """
        获取分组或全局成员脸谱uuid
        :return:
        """
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT makeup.face_uuid 
                FROM faceU_faceufacialmakeupmapping AS mapping 
                JOIN faceU_faceufacialmakeup AS makeup 
                ON mapping.face_id = makeup.id
                WHERE 1={1 if self._overall_situation else 0} or mapping.group_id = {self._group}
            """)

            row = cursor.fetchall()
        return '@'.join([rw[0] for rw in row])

    def from_face_uuid(self, face_uuid):
        """
        从uuid获取成员信息
        :param face_uuid:
        :return:
        """
        face_uuid = face_uuid.split('@')
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT mapping.id, mapping.name, mapping.code 
                FROM faceU_faceufacialmakeupmapping AS mapping 
                JOIN faceU_faceufacialmakeup AS makeup 
                ON mapping.face_id = makeup.id
                WHERE (1={1 if self._overall_situation else 0} or mapping.group_id = {self._group})
                AND makeup.face_uuid in ({"'" + "','".join(face_uuid) + "'"})
            """)

            row = cursor.fetchall()
        return [{
            'id': rw[0],
            'name': rw[1],
            'code': rw[2],
        } for rw in row]
