# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class JenkinsJob(models.Model):
    """
    Jenkins Job Log
    """
    job_name = models.TextField(default=None, null=True, blank=True)
    params = models.TextField(default=None, null=True, blank=True)
    number = models.IntegerField(default=None, null=True, blank=True)
    status = models.CharField(max_length=20, default=0, null=True, blank=True)
    time = models.CharField(max_length=100, default=None, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'jenkins_job'
        verbose_name = 'jenkins_job'
        verbose_name_plural = 'jenkins_job'