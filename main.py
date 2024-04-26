import time

from authlib.oauth2 import OAuth2Error
from flask import Blueprint, render_template, redirect, request, session, url_for
from flask_login import login_required, current_user
from werkzeug.security import gen_salt

from . import db
from .models import OAuth2Client, User
from .oauth2 import authorization, require_oauth

main = Blueprint('main', __name__)


def get_session_user():
    if 'user_id' not in session:
        return None
    user_id = session.get('user_id')
    return user_id


def split_function(s):
    return [v for v in s.splitlines() if v]


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/new_client', methods=('GET', 'POST'))
def new_client():
    user_id = get_session_user()
    if not user_id:
        return redirect('/')
    if request.method == 'GET':
        return render_template('new_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user_id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_function(form["grant_type"]),
        "redirect_uris": split_function(form["redirect_uri"]),
        "response_types": split_function(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()
    return redirect('/')


@main.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    if not user:
        return redirect(url_for('home.home', next=request.url))
    if request.method == 'GET':
        try:
            grant = authorization.get_consent_grant(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)
