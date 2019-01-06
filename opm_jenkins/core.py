# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from channels import Group
from jenkinsapi.jenkins import Jenkins
import utils
import json
import time
import uuid


class JenkinsApi(utils.Utils):
    def __init__(self, job_name):
        self._jenkins = self.get_instance()
        self._job_name = job_name
        self._job = self.get_job()
        self._build = None
        self.last_build_number = self.get_last_completed_buildnumber()
        self.status = 'Unknown'
        self.row_id = None
        self.save_func = self.save

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

    def build_job(self, params, callback=None):
        params['uuid'] = str(int(round(time.time()*1000)))  # uuid.uuid1()
        if self._do_method("build_job", params=params):
            number = self._get_buildnumber(params)
            if number:
                if self.row_id:
                    self._log_start(number, params['uuid'])
                else:
                    self.row_id = self._get_row_id(number, params, callback)
                while True:
                    self.update_build(number)
                    if self.is_running():
                        time.sleep(2)
                        self._log_running()
                    else:
                        break
                self._log_stop()
            else:
                self.status = 'ERROR_NUMBER'
                self._log_error()
        else:
            if self.row_id: self._log_error()
        return self.status

    def _get_buildnumber(self, params):
        for i in range(5):
            buildnumber = None
            lastest_build_number = self.get_last_buildnumber()
            while True:
                if lastest_build_number <= self.last_build_number:
                    time.sleep(2)
                    lastest_build_number = self.get_last_buildnumber()
                else:
                    break
            for number in range(self.last_build_number, lastest_build_number + 1):
                build = self.get_build(number)
                parameters = self._get_params(build)
                if parameters.has_key('uuid'):
                    if parameters['uuid'] == params['uuid']:
                        self._build = build
                        buildnumber = number
                        break
            if buildnumber:
                break
            else:
                time.sleep(2)
        return buildnumber

    def _get_params(self, build):
        actions = build._data.get('actions')
        for elem in actions:
            if elem.has_key('parameters'):
                parameters = elem.get('parameters', {})
            else:
                break
        return {pair['name']: pair.get('value') for pair in parameters}

    def build_job_log(self, params, row_id=None, save_func=None):
        self.row_id = row_id
        self.save_func = save_func
        return self.build_job(params, callback=None)

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
                    status = 'Building'
        return status

    def update_status(self):
        pass

    def _get_row_id(self, number, params, callback):
        data = {
            "job_name": self._job_name,
            "uuid": params.pop('uuid'),
            "callback": callback,
            "parameters": json.dumps(params),
            "number": number,
            "status": self.get_building_status()
        }
        data.update(params)
        return self.save_func('create', data)['instance'].id

    def _ws_send(self, status):
        Group(self._job_name + str(self.row_id)).send({'text': json.dumps({"status": status})})

    def _save(self, data):
        return self.save_func('update', data, id=self.row_id)

    def _log_start(self, number, uuid):
        status = self.get_building_status()
        self.status = status
        self._ws_send(status)
        return self._save(dict(
            uuid=uuid,
            number=number,
            status=status
        ))

    def _log_running(self):
        status = self.get_building_status()
        if self.status == status:
            pass
        else:
            self._ws_send(status)
            self.status = status
            self._save(dict(status=status))

    def _log_stop(self):
        status = self.get_building_status()
        self.status = status
        self._ws_send(status)
        return self._save(dict(
            status=status,
            took_time=self.get_duration()
        ))

    def _log_error(self):
        status = self.status
        self._ws_send(status)
        return self._save(dict(
            status=status,
            took_time="0"
        ))

