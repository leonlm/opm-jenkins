# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import *
import json


class JenkinsBuildLogSerializerR(serializers.ModelSerializer):
    parameters = serializers.SerializerMethodField()
    callback = serializers.SerializerMethodField()

    class Meta:
        model = JenkinsBuildLog
        fields = '__all__'

    def get_parameters(self, obj):
        if obj.parameters:
            parameters = json.loads(obj.parameters)
        else:
            parameters = None
        return parameters

    def get_callback(self, obj):
        if obj.callback:
            callback = json.loads(obj.callback)
        else:
            callback = None
        return callback


class JenkinsBuildLogSerializerCU(serializers.ModelSerializer):

    class Meta:
        model = JenkinsBuildLog
        fields = '__all__'