from flask import Blueprint, redirect, url_for, session, request, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db
import requests
import os

auth_bp = Blueprint("auth", __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@auth_bp.route("/login")
def login():
    from oauthlib.oauth2 import WebApplicationClient
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    google_cfg = get_google_provider_cfg()
    authorization_endpoint = google_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for("auth.callback", _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth_bp.route("/callback")
def callback():
    from oauthlib.oauth2 import WebApplicationClient
    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    code = request.args.get("code")
    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for("auth.callback", _external=True),
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(token_response.text)

    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()

    google_id = userinfo["sub"]
    name = userinfo["name"]
    email = userinfo["email"]
    avatar = userinfo.get("picture")

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(google_id=google_id, name=name, email=email, avatar=avatar)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("main.home"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
