import time

from flask import Blueprint, render_template, redirect, request, session
from flask_login import login_required, current_user
from werkzeug.security import gen_salt

from . import db
from .models import OAuth2Client

main = Blueprint('main', __name__)


def get_session_user():
    if 'id' not in session:
        return None
    user_id = session['user_id']
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
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        return render_template('new_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
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
