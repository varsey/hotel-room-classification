import h2o

from src.modules.logger import DicLogger, LOGGING_CONFIG

log = DicLogger(LOGGING_CONFIG).log


def init_h2o():
    h2o.init(verbose=False)
    log.info(f'{h2o.cluster().show_status()}')
    h2o.no_progress()
    return h2o
