# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from utils import JenkinsApi


@task
def jenkins_job(request_data):
    jenkins = JenkinsApi(request_data['job_name'])
    jenkins.build_job(request_data['params'])