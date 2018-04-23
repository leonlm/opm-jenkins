# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from serializers import *


def get_serializer_class():
    return JenkinsJobSerializer

def get_queryset():
    return JenkinsJob

def save(method, request_data, **kwargs):
    if method == "create":
        serializer = JenkinsJobSerializer(data=request_data)
    else:
        if kwargs.get('instance', False):
            instance = kwargs.pop('instance')
        else:
            instance = JenkinsJob.objects.get(**kwargs)
        serializer = JenkinsJobSerializer(instance, data=request_data, partial=True)

    if serializer.is_valid():
        instance_save = serializer.save()
        retdict = {'status': 1, 'data': serializer.data, "msg": "SUCCESS", "instance": instance_save}
    else:
        retdict = {"status": 0, "data": "", "msg": "ERROR,"+json.dumps(serializer.errors)}
    return retdict