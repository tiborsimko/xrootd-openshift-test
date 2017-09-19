FROM centos:7
RUN yum install -y epel-release
RUN yum install -y \
    python-pip \
    xrootd \
    xrootd-client \
    xrootd-client-devel \
    xrootd-python
RUN pip install xrootdpyfs
ADD test.py /tmp/test.py
CMD ["/usr/bin/python", "/tmp/test.py"]
