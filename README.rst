.. image:: https://travis-ci.org/tiborsimko/xrootd-openshift-test.png
   :target: https://travis-ci.org/tiborsimko/xrootd-openshift-test
.. image:: https://img.shields.io/badge/licence-GPL_3-green.svg?style=flat
   :target: https://raw.githubusercontent.com/tiborsimko/xrootd-openshift-test/master/COPYING

Testing XRootD container on OpenShift
-------------------------------------

Running locally
```````````````

Firstly, on laptop, test using bare docker as follows::

  $ docker build -t xrootd-openshift-test .
  $ docker run --rm xrootd-openshift-test
  OK

Secondly, on OpenShift, test as follows::

OpenShift tests
```````````````

Using OpenShift build
'''''''''''''''''''''
Login to Openshift using CERN credentials::

  $ oc login https://openshift.cern.ch


Create resources contained under `openshift` directory::

  $ oc create -f openshift/xrootdpyfs-output-image.yaml
  imagestream "xrootdpyfs" created
  $ oc create -f openshift/xrootdpyfs-build.yaml
  buildconfig "xrootdpyfs-build" created
  $ oc create -f openshift/xrootdpyfs-deployment.yaml
  deploymentconfig "xrootdpyfs" created


Once the resources are created, as if you were runing `docker build .` locally, run::

  $ oc start-build xrootdpyfs-build --follow
  build "xrootdpyfs-build-1" started
  timed out getting logs, retrying
  Cloning "https://github.com/tiborsimko/xrootd-openshift-test" ...
          Commit: aa9c71b821f2cd39f050af153272d5e483a94198 (docs: nicer README)
          Author: Tibor Simko <tibor.simko@cern.ch>
          Date:   Tue Sep 19 18:18:55 2017 +0200
  Pulling image docker.io/centos@sha256:822de5245dc5b659df56dd32795b08ae42db4cc901f3462fc509e91e97132dc0 ...
  Pulled 0/1 layers, 7% complete
  Pulled 1/1 layers, 100% complete
  ...


Finally, run the test case::

  $ oc debug dc/xrootdpyfs
  Debugging with pod/xrootdpyfs-debug, original command: /usr/bin/python /tmp/test.py
  Waiting for pod to start ...
  sh-4.2$ python /tmp/test.py
  Segmentation fault # hopefully OK when fixed


Using locally built image
'''''''''''''''''''''''''

Building image locally and pushing to Dockerhub::

  $ docker build . -t <dockerhub-username>/xrootd-openshift
  $ docker push <dockerhub-username>/xrootd-openshift
  # replace <dockerhub-username> with real one in
  # `xrootdpyfs-from-dockerhub-deployment.yaml`
  $ oc create -f openshift/xrootdpyfs-from-dockerhub-deployment.yaml
  $ oc debug dc/xrootdpyfs-from-dockerhub
  Debugging with pod/xrootdpyfs-from-dockerhub-debug, original command: /usr/bin/python /tmp/test.py
  Waiting for pod to start ...
  Pod IP: 10.76.22.243
  If you don't see a command prompt, try pressing enter.
  sh-4.2$ python /tmp/test.py
  Segmentation fault


Building xrootd from sources
''''''''''''''''''''''''''''

Replacing dockerfile name in `xrootdpyfs-build.yaml` for `Dockerfile-building-xrootd-from-sources`::

  $ oc create -f openshift/xrootdpyfs-output-image.yaml
  imagestream "xrootdpyfs" created
  $ oc create -f openshift/xrootdpyfs-build.yaml
  buildconfig "xrootdpyfs-build" created
  $ oc create -f openshift/xrootdpyfs-deployment.yaml
  deploymentconfig "xrootdpyfs" created
  $ oc start-build xrootdpyfs-build --follow
  $ oc debug dc/xrootdpyfs
  Debugging with pod/xrootdpyfs-from-sources-debug, original command: /usr/bin/python /tmp/test.py
  Waiting for pod to start ...
  Pod IP: 10.76.8.146
  If you don't see a command prompt, try pressing enter.
                                                      sh-4.2$
  sh-4.2$ python /tmp/test.py
  Segmentation fault


Running locally with random user
''''''''''''''''''''''''''''''''

Build CentOS 7 image locally and run it::

  $ docker build -t xrootd-openshift-test-centos7 . -f Dockerfile-centos7
  $ docker run --rm --user 9999 xrootd-openshift-test-centos7 bash
  bash-4.2$ python /tmp/test.py
  Segmentation fault
  bash-4.2$ python -c 'import xrootdpyfs'
  Segmentation fault
  bash-4.2$ python -c 'import XRootD.client'
  Segmentation fault


Final fix: naming random user at run time
'''''''''''''''''''''''''''''''''''''''''

Following (OpenShift docs)[https://docs.openshift.org/latest/creating_images/guidelines.html#openshift-origin-specific-guidelines], we will use `uid_entrypoint` script to name the user at run time. See `Dockerfile-centos7-name-user-at-runtime`::

  $ docker build -t xrootd-openshift-test-centos7 . -f Dockerfile-centos7-name-user-at-runtime
  $ docker run --rm --user 9999 xrootd-openshift-test-centos7 python /tmp/test.py
  OK
