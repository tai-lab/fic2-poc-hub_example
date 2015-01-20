import sys, os, io, logging
from pkg_resources import resource_stream
import lya
from foobar import app


def _setup_basic_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.INFO)
    logger.addHandler(steam_handler)
    return [logger, steam_handler]

def _update_configuration(cfg, logger):
    path = os.getenv('FOOBAR_API_CONF_FILEPATH')
    if path is not None and os.path.isfile(path):
        logger.info(' * Updating configuration with {}'.format(path))
        cfg.update_yaml(path)
    else:
        logger.info(' * Ignoring configuration {}={}'.format('FOOBAR_API_CONF_FILEPATH', path))

def _load_configuration(logger):
    logger.info(' * Configuration ...')
    conf = lya.AttrDict.from_yaml(resource_stream('foobar.resources', 'foobar.default.yml'))
    _update_configuration(conf, logger)
    f = io.StringIO()
    conf.dump(f)
    logger.info(f.getvalue())
    return conf

_logger, _handler = _setup_basic_logging()
cfg = _load_configuration(_logger)
_handler.close()
_logger.removeHandler(_handler)
