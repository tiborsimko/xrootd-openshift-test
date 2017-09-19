#!/usr/bin/env python
from xrootdpyfs import XRootDPyFS
fs = XRootDPyFS("root://eospublic.cern.ch//eos/opendata/cms/Run2011A/BTag/AOD/12Oct2013-v1/20000/")
filelist = fs.listdir("")
assert 'D69FF34D-FD3D-E311-95A0-002618943913.root' in filelist
print 'OK'
