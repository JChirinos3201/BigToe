#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/BigToe/')
sys.path.insert(1, '/var/www/BigToe/BigToe')

from BigToe import app as application
application.secret_key = 'FHsWHwCb5dX9UJCUK1LPq8BSVnHKP6kA'
