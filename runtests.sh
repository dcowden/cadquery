#!/bin/sh
export PYTHONDONTWRITEBYTECODE=1
CQ_BACKEND=pythonOCC && py.test -s --cov
