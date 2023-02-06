"""Application Entrypoint.
"""

import logging
from . import make_app


# Configure Logging
FORMAT = "%(asctime)s:%(module)s:%(funcName)s:%(levelname)s:%(message)s"
LEVEL = logging.DEBUG

logger = logging.getLogger("freejay")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LEVEL)
formatter = logging.Formatter(fmt=FORMAT)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Start Application
make_app()
