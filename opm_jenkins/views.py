# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import django_filters
from rest_framework import viewsets
from django.http.response import JsonResponse
from utils import Utils
import json
import tasks


class JenkinsBuildLogViewSet(viewsets.ModelViewSet, Utils):
    def get_serializer_class(self):
        return self.get_serializer_list()
        
    def get_queryset(self):
        return self.get_model().objects.all()

    def _format(self, request):
        return {
            'job_name': request.data['job_name'],
            'parameters': json.dumps(request.data['parameters'])
        }

    def create(self, request, *args, **kwargs):
        retdict = Utils.save('create', self._format(request))
        if retdict['status'] == 1:
            row_id = retdict.pop('instance').id
            tasks.build.apply_async((request.data, row_id),
                retry=True,
                retry_policy={
                    'max_retries': 3,
                    'interval_start': 1,
            })
        return JsonResponse(retdict, status=200)
