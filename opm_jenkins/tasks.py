# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from utils import save


@task
def jenkins_job():
    pass