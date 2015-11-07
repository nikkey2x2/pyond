import logging

logger = logging.getLogger(__package__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(message)s',
                              datefmt='%d.%m.%Y %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)
