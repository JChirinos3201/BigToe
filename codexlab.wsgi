#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/codexlab/')
sys.path.insert(1, '/var/www/codexlab/codexlab/')

from codexlab import app as application
application.secret_key = 'FHsWHwCb5dX9UJCUK1LPq8BSVnHKP6kA'
