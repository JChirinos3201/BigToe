import authlib
import flask

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHOIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

@app.route("/")
def home():
    session = authlib.client.OAuth2Session('512483857995-lkdjkkk0ek9rifhibqi5if082oq65mf7.apps.googleusercontent.com', 'zaBlmol-Ks8Lf3KBKsT7bYyH',redirect_uri='http://localhost:5000')
    
    uri,state=session.authorization_url(AUTHORIZATION_URL)

    flask.session["auth_state"]=state
    flask.session.permanent=True

    return flask.redirect(uri,code=302)

@app.route("/second")
def redirect():
    state=flask.request.args.get("state",default=None,type=None)

    if state != flask.session["auth_state"]:
        return flask.render_template("j.html",something="Uhh you done messed up")
    session = authlib.client.OAuth2Session('512483857995-lkdjkkk0ek9rifhibqi5if082oq65mf7.apps.googleusercontent.com', 'zaBlmol-Ks8Lf3KBKsT7bYyH',redirect_uri='http://localhost:5000')

    oauth2_tokens = session.fetch_access_token(ACCESS_TOKEN_URI,authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY]=oauth2_tokens

    return flask.render_template("j.html",oauth_tokens)

