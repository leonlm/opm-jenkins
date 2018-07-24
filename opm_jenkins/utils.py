# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from serializers import *


class Utils(object):
    def get_serializer_list(self):
        return JenkinsBuildLogSerializerR

    def get_serializer_cu(self):
        return JenkinsBuildLogSerializerCU

    def get_model(self):
        return JenkinsBuildLog

    def save_utils(self, method, request_data, **kwargs):
        if method == "create":
            serializer = self.get_serializer_cu()(data=request_data)
        else:
            if kwargs.get('instance', False):
                instance = kwargs.pop('instance')
            else:
                instance = self.get_model().objects.get(**kwargs)
            serializer = self.get_serializer_cu()(instance, data=request_data, partial=True)

        if serializer.is_valid():
            instance_save = serializer.save()
            retdict = {'status': 1, 'data': serializer.data, "msg": "SUCCESS", "instance": instance_save}
        else:
            retdict = {"status": 0, "data": "", "msg": "ERROR,"+json.dumps(serializer.errors)}
        return retdict

    def filter_utils(self, **kwargs):
        return self.get_serializer_list()(self.get_model().objects.filter(**kwargs), many=True).data
