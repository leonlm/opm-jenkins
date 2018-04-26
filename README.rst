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

- ``JENKINS_JOB``

JENKINS_JOB = {
    'job_name': 'job_name'
    
}

- ``USER_ID``

USER_ID = 'username'

- ``API_TOKEN``

API_TOKEN = 'Api Token'



Settings
--------


Changelog
---------

