## How to use

Login to Openshift using CERN credentials:

```console
$ oc login https://openshift.cern.ch
```

Create resources contained under `openshift` directory:

```console
$ oc create -f openshift/xrootdpyfs-output-image.yaml
imagestream "xrootdpyfs" created
$ oc create -f openshift/xrootdpyfs-build.yaml
buildconfig "xrootdpyfs-build" created
$ oc create -f openshift/xrootdpyfs-deployment.yaml
deploymentconfig "xrootdpyfs" created
```

Once the resources are created, as if you were runing `docker build .` locally, run:

```console
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
```

Finally, run the test case:

```console
$ oc debug dc/xrootdpyfs
Debugging with pod/xrootdpyfs-debug, original command: /usr/bin/python /tmp/test.py
Waiting for pod to start ...
sh-4.2$ python /tmp/test.py
Segmentation fault # hopefully OK when fixed
```
