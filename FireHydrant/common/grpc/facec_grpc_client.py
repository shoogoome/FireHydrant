import grpc
from .model import faceRecognition_pb2, faceRecognition_pb2_grpc
from common.utils.hash.signatures import generate_token
import time
from common.exceptions.grpc.info import FireHydrantFaceUGrpcExcept
import logging

def auth_token():
    payload = {
        'create_time': time.time()
    }
    return generate_token(payload)


class FireHydrantFacecRecognitionClient(object):

    def __init__(self):
        """
        人脸识别grpc客户端
        """
        self.ip = "172.31.139.156"
        self.port = "8001"
        self.conn = "{}:{}".format(self.ip, self.port)

    def is_exists(self, face_image):
        """
        查询人脸是否存在
        :param face_image:
        :return:
        """
        try:
            auth = faceRecognition_pb2.Auth(token=auth_token())
            request = faceRecognition_pb2.faceData(image=face_image, auth=auth)

            with grpc.insecure_channel(self.conn) as channel:
                stub = faceRecognition_pb2_grpc.FaceRecognitionStub(channel)
                response = stub.is_exists(request)

                return response.uuid
        except Exception as ex:
            logging.error(ex)
            raise FireHydrantFaceUGrpcExcept.server_except()

    def upload_face(self, face_image, uuid):
        """
        上传人脸
        :param face_image:
        :param uuid:
        :return:
        """
        try:
            auth = faceRecognition_pb2.Auth(token=auth_token())
            request = faceRecognition_pb2.faceData(
                image=face_image, uuid=uuid, auth=auth)

            with grpc.insecure_channel(self.conn) as channel:
                stub = faceRecognition_pb2_grpc.FaceRecognitionStub(channel)
                response = stub.upload_face(request)

                return response.uuid
        except Exception as ex:
            logging.error(ex)
            raise FireHydrantFaceUGrpcExcept.server_except()

    def recognition(self, image, face_list):
        """
        识别
        :param image:
        :param face_list:
        :return:
        """
        try:
            # re
            auth = faceRecognition_pb2.Auth(token=auth_token())
            request = faceRecognition_pb2.faceMessage(
                image=image, face_list=face_list, auth=auth)

            with grpc.insecure_channel(self.conn) as channel:
                stub = faceRecognition_pb2_grpc.FaceRecognitionStub(channel)
                response = stub.recognition(request)

                return response.face_list, response.image
        except Exception as ex:
            logging.error(ex)
            raise FireHydrantFaceUGrpcExcept.server_except()

