import logging

logger = logging.getLogger("freejay")
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter("%(name)s:%(levelname)s:%(message)s"))
logger.addHandler(log_handler)
