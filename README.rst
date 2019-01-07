opm-jenkins
==============

Plug and play continuous integration with Django REST framework and Jenkins


Installation
------------

Downloading the source and running::

    $ python setup.py install

Latest git version::

    $ pip install -e git+git://github.com/leonlm/opm-jenkins.git#egg=opm-jenkins



Usage
-----

Add ``'opm_jenkins'`` to your ``INSTALLED_APPS`` list.

Add ``settings.py``

- ``JENKINS``

JENKINS = {
    'JENKINS_URL': "http://server_ip:port",
    'USER_ID': "username",
    'API_TOKEN': "Api Token"
}



Settings
--------


Changelog
---------
v1.2.2
    1. update

v1.2.1
    1. support private table

v1.2.0
    1. websocket support

v1.1.1
    1. Update

v1.1.0
    1. Add other model

v1.0.1
    1. Update
    
v1.0.0
    1. Fix

v0.2
    1. Update

v0.1
    1. Initial version
