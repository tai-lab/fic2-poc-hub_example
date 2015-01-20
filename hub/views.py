import uuid
from hub import app
from hub.user import User
from flask import request, render_template, session, redirect, url_for
from flask.ext.login import login_required, login_user, current_user

@app.route('/')
@login_required
def root():
    return render_template('index.html', current_user_id=current_user.id)


@app.route('/authorize')
def authorize():
    resp = app.remote.authorized_response()
    if resp is None:
        default = 'Unable the check authorization with remote'
        msg = 'reason=%s error=%s' % (
            request.args.get('error_reason', default), request.args.get('error_description', default))
        data = {'title': 'Access denied', 'msg': msg}
        return render_template('error.html', **data)
    app.logger.info('OAuth response: %s', resp)
    d_user = {'access_token': resp['access_token'], 'refresh_token': resp['refresh_token'], 'id': str(uuid.uuid4())}
    session['remote_oauth'] = d_user
    login_user(User(d_user))
    return redirect(url_for('root', _scheme="https", _external=True))
