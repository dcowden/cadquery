#!/bin/sh
CQ_BACKEND=pythonOCC && py.test -s --cov
CQ_BACKEND=FreeCAD && py.test -s --cov
