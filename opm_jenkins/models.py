# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class JenkinsBuildLog(models.Model):
    """
    Jenkins Job Build Log
    """
    job_name = models.TextField(default=None, null=True, blank=True)
    parameters = models.TextField(default=None, null=True, blank=True)
    uuid = models.CharField(max_length=128, default=None, null=True, blank=True)
    number = models.IntegerField(default=None, null=True, blank=True)
    status = models.CharField(max_length=16, default='Start', null=True, blank=True)
    duration = models.CharField(max_length=100, default=None, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    callback = models.TextField(default=None, null=True, blank=True)
    # console = models.TextField(default=None, null=True, blank=True)

    class Meta:
        ordering = ('-start_time',)
        db_table = 'JenkinsBuildLog'
        verbose_name = 'JenkinsBuildLog'
        verbose_name_plural = 'JenkinsBuildLog'
