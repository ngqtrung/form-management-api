import logging

log = logging.getLogger("FormManagementAPI")


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s --  %(levelname)s  -- %(message)s"))
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
