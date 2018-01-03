#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

if os.environ['PYPEEP_IP'] and os.environ['PYPEEP_PORT']:
    import pydevd
    pydevd.settrace(os.environ['PYPEEP_IP'], port=int(os.environ['PYPEEP_PORT']), stdoutToServer=True, stderrToServer=True)
