# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from jenkinsapi.jenkins import Jenkins
import json
import time
import uuid
import ast
import utils

class JenkinsApi(utils.Utils):
    def __init__(self, job_name, row_id=None):
        self._jenkins = self.get_instance()
        self._job_name = job_name
        self._row_id = row_id
        self._job = self.get_job()
        self._build = None
        self.last_build_number = self.get_last_completed_buildnumber()
        self.status = 'Unknown'

    @classmethod
    def get_instance(self):
        for i in range(5):
            try:
                instance = Jenkins(
                    settings.JENKINS['JENKINS_URL'], 
                    username=settings.JENKINS['USER_ID'], 
                    password=settings.JENKINS['API_TOKEN']
                )
                self.status = 'JENKINS'
                break
            except:
                instance = None
                self.status = 'ERROR_JENKINS'
                time.sleep(2)
        return instance

    def get_job(self):
        if self._jenkins:
            job = self._jenkins.get_job(self._job_name)
            self.status = 'JOB'
        else:
            job = None
            self.status = 'ERROR_JOB'
        return job

    def _do_method(self, func, **kwargs):
        if self._jenkins and self._job:
            if func == "get_last_completed_buildnumber":
                result = self._job.get_last_completed_buildnumber()
            elif func == "get_last_buildnumber":
                result = self._job.get_last_buildnumber()
            elif func == "build_job":
                params = kwargs.get('params', False)
                self._jenkins.build_job(self._job_name, params)
                result = "Building"
            elif func == "get_build":
                params = kwargs.get('params', False)
                result = self._job.get_build(params)
            elif func == "is_queued":
                result = self._job.is_queued()
            elif (self._build and func == "get_result_url"):
                result = self._build.get_result_url()
            elif (self._build and func == "get_console"):
                result = self._build.get_console()
            elif (self._build and func == "get_status"):
                result = self._build.get_status()
            elif (self._build and func == "is_running"):
                result = self._build.is_running()
            else:
                result = None
        else:
            result = None
        return result

    def build_job(self, params):
        params['uuid'] = str(int(round(time.time()*1000)))  # uuid.uuid1()
        if self._do_method("build_job", params=params):
            number = self._get_buildnumber(params)
            if self._row_id:
                self._log_start(number, params['uuid'])
            else:
                self._row_id = self._get_row_id(number, params)
            
            while True:
                self.update_build(number)
                if self.is_running():
                    time.sleep(2)
                    self._log_running()
                else:
                    break
            self._log_stop()
        return self.status

    def _get_buildnumber(self, params):
        lastest_build_number = self.get_last_buildnumber()
        while True:
            if lastest_build_number <= self.last_build_number:
                time.sleep(2)
                lastest_build_number = self.get_last_buildnumber()
            else:
                break
        buildnumber = None
        for number in range(self.last_build_number, lastest_build_number + 1):
            build = self.get_build(number)
            if build.get_params()['uuid'] == params['uuid']:
                self._build = build
                buildnumber = number
                break
        return buildnumber

    def get_last_completed_buildnumber(self):
        return self._do_method("get_last_completed_buildnumber")

    def get_last_buildnumber(self):
        return self._do_method("get_last_buildnumber")

    def get_build(self, buildnumber):
        return self._do_method("get_build", params=buildnumber)
        
    def update_build(self, number):
        self._build = self.get_build(number)
        return True
        
    def get_status(self):
        return self._do_method("get_status")

    def get_duration(self):
        return self.get_data()['duration']

    def is_running(self):
        return self._do_method("is_running")

    def is_queued(self):
        return self._do_method("is_queued")

    def get_data(self):
        return self._build._data

    def get_result_url(self):
        return self._do_method("get_result_url")
    def get_console(self):
        return self._do_method("get_console")

    def get_building_status(self):
        if self.is_queued():
            status = 'Queued'
        else:
            if self.is_running():
                status = 'Building'
            else:
                if self.get_status() == 'SUCCESS':
                    status = 'Stop'
                elif self.get_status() == 'FAILURE':
                    status = 'Failure'
                else:
                    status = 'Unknown'
        self.status = status
        return self.status

    def _get_row_id(self, number, params):
        data = {
            "job_name": self._job_name,
            "uuid": params.pop('uuid'),
            "parameters": json.dumps(params),
            "number": number,
            "status": self.get_building_status()
        }
        return self.save_utils('create', data)['instance'].id

    def _save(self, data):
        return self.save_utils('update', data, id=self._row_id)

    def _log_start(self, number, uuid):
        return self._save(dict(
            uuid = uuid,
            number = number,
            status = self.get_building_status()
        ))

    def _log_running(self):
        return self._save(dict(status=self.get_building_status()))
    
    def _log_stop(self):
        return self._save(dict(
            status = self.get_building_status(),
            took_time = self.get_duration()
        ))