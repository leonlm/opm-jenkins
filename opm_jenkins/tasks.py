# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from .core import JenkinsApi


@task
def build(request_data, row_id):
    jenkins = JenkinsApi(request_data['job_name'], row_id=row_id)
    jenkins.build_job(request_data['parameters'])


@task
def buildlog(request_data):
    jenkins = JenkinsApi(request_data['job_name'])
    jenkins.build_job(request_data['parameters'])