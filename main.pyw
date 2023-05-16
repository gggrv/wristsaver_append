# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

log.setLevel( logging.DEBUG )

# embedded in python
import os
import sys
# pip install
# same project
from wristsaver.pyqt5.Application import Application

def autorun():
    ob = Application( sys.argv )

if __name__ == '__main__':
    autorun()

#---------------------------------------------------------------------------+++
# end 2023.05.14
# created
