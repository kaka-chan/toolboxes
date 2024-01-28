#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    :  2021/12/7 13:00
# @Author  :  cjh
# @Email   :  775077403@qq.com
try:
    from cStringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO
from onvif import ONVIFCamera
import cv2
import requests
import numpy as np
from requests.auth import HTTPDigestAuth


class Camera:
    """This class is used to get the information from all cameras discovered on this specific
    network."""
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.username = user
        self.password = password

        self.is_moving = False
        self.cam = ONVIFCamera(ip, port, user, password)
        # Create media service object
        self.media = self.cam.create_media_service()
        # Get target profile
        self.media_profile = self.media.GetProfiles()[0]
        self.media_profile_token = {'ProfileToken': self.media_profile.token}
        self.snapshot_url = self.media.GetSnapshotUri(self.media_profile_token).Uri
        self.rtsp_url = self.get_rtsp()

    def get_rtsp(self):
        """
        获取摄像头rtsp地址
        :return: rtsp地址
        """
        obj = self.media.create_type('GetStreamUri')
        obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        obj.ProfileToken = self.media_profile.token
        res_uri = self.media.GetStreamUri(obj)['Uri']
        return res_uri

    def snapshot_cut(self, timeout=3):
        """
        获取摄像头截图
        :param timeout: 请求最大耗时，超时将报错
        :return: 二进制图像, 可以直接wb模式写文件
        """
        response = requests.get(self.snapshot_url, auth=HTTPDigestAuth(self.username, self.password), timeout=timeout)
        return response.content

    @staticmethod
    def binary2cv(binary_image, image_type=np.uint8):
        """
        将二进制图像转为cv2格式的图像
        :param binary_image: 二进制图像
        :param image_type: 图像类型
        :return: 返回cv2格式的图像
        """
        return cv2.imdecode(np.frombuffer(binary_image, image_type), 1)
