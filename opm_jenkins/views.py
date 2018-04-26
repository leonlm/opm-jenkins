# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import django_filters
from rest_framework import viewsets
from django.http.response import JsonResponse
from utils import (
    get_serializer_class,
    get_queryset,
    save
)
from tasks import jenkins_job


class JenkinsJobViewSet(viewsets.ModelViewSet):
    serializer_class = get_serializer_class()
    queryset = get_queryset().objects.all()

    def create(self, request, *args, **kwargs):
        retdict = save("create", request.data)
        if retdict['status'] == 1 and retdict.has_key('instance'):
            retdict.pop('instance')
            jenkins_job.apply_async((request.data),
                retry=True,
                retry_policy={
                    'max_retries': 3,
                    'interval_start': 1,
            })
        return JsonResponse(retdict, status=200)
