# -*- coding: utf-8 -*-

import sys
import os

# run in right directory
if not sys.argv[0]:
    appdir = os.path.abspath(os.path.dirname(__file__))
else:
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))


appdir = os.path.abspath(os.path.join(appdir, os.pardir, os.pardir))

if not appdir in sys.path:
    sys.path.insert(0, appdir)





