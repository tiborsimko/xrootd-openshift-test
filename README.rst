Testing XRootD container on OpenShift
-------------------------------------

Firstly, on laptop, test using bare docker as follows::

  $ docker build -t xrootd-openshift-test .
  $ docker run --rm xrootd-openshift-test
  OK

Secondly, on OpenShift, test as follows::

  FIXME
