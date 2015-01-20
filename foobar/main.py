import logging
import http
from foobar import app
from foobar.configuration import cfg
from foobar.user import User
from flask import request, session
from flask_oauthlib.client import OAuth


def _setup_logging(app):
    level = logging.getLevelName(cfg.level)
    # logging.getLogger('foobar').setLevel(level)
    app.logger.setLevel(level)
    sh = logging.StreamHandler()
    sh.setLevel(cfg.level)
    target_loggers = [logging.getLogger('flask_oauthlib'), logging.getLogger('requests.packages.urllib3')]
    for logger in target_loggers:
        logger.setLevel(level)
        logger.addHandler(sh)
    # http.client.HTTPConnection.debuglevel = 1


def _register_remote(app):
    if cfg.oauth:
        oauth = OAuth(app)
        remote = oauth.remote_app(
            "oauth-remote",
            consumer_key=cfg.oauth.consumer_key,
            consumer_secret=cfg.oauth.consumer_secret,
            request_token_params=cfg.oauth.request_token_params,
            base_url=cfg.oauth.base_url,
            request_token_url=cfg.oauth.request_token_url,
            access_token_url=cfg.oauth.access_token_url,
            access_token_method=cfg.oauth.access_token_method,
            authorize_url=cfg.oauth.authorize_url
            )
        app.remote = remote
        app.logger.info(
            "The remote app '{}' has been registered".format(remote.name))
    else:
        raise RuntimeError(
            "No remote app configured for OAuth, check the yaml files")


def main():
    _setup_logging(app)
    _register_remote(app)
    app.run(debug=cfg.debug, host=cfg.host, port=cfg.port)


@app.after_request
def add_header(response):
    """ Intercept response to bypass browser cache and
    add extra logging for redirection.
    """
    if response.status_code in [301, 302, 303, 307]:
        msg = "Detecting a redirection {}; Location: {}".format(
            response.status_code, response.headers['Location'])
        app.logger.info(msg)
    if request.path.startswith('/static/lib/'):
        return response
    if cfg.debug:
        response.cache_control.max_age = 0
        response.cache_control.no_store = True
        response.cache_control.no_cache = True
    return response


@app.login_manager.user_loader
def load_user(userid):
    app.logger.info('>> load_user {}'.format(userid))
    tmp = session.get('remote_oauth')
    if tmp:
        return User(tmp)
    return None

@app.login_manager.unauthorized_handler
def unauthorized():
    return app.remote.authorize(callback=cfg.callback_url)
