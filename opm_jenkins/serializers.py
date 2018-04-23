# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import *


class JenkinsJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = JenkinsJob
        fields = '__all__'
