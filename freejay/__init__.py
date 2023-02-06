"""
Python FreeJay is an open source DJ application.
"""

import logging
from freejay.app import make_app

logging.getLogger(__name__).addHandler(logging.NullHandler())
