# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from channels import Group
from channels.sessions import enforce_ordering


@enforce_ordering
def ws_connect(message, *args, **kwargs):
    Group(kwargs['job_name'] + kwargs['row_id']).add(message.reply_channel)
    message.reply_channel.send({"accept": True})


@enforce_ordering
def ws_disconnect(message, *args, **kwargs):
    Group(kwargs['job_name'] + kwargs['row_id']).discard(message.reply_channel)