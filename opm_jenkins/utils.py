# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from serializers import *
from django.conf import settings
from jenkinsapi.jenkins import Jenkins
import time


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
    

class JenkinsApi(object):
    def __init__(self, job_name):
        """
        Initialize a jenkins connection
        """
        instance = self.get_instance()
        self._jenkins = instance
        self._job_name = job_name
        self._job = self.get_job(instance, job_name)
        self._build = None

    @classmethod
    def get_instance(self):
        for i in range(5):
            try:
                instance = Jenkins(settings.JENKINS_URL, username=settings.USER_ID, password=settings.API_TOKEN)   # Represents a jenkins environment.
                break
            except:
                instance = None
                time.sleep(2)
        return instance
        
    def build_job(self, params):
        self._jenkins.build_job(self._job_name, params=params)
        
    def update_log(self, params):
        pass
        
        
        
        