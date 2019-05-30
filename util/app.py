import authlib
import flask

ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
AUTHOIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

try:
    f=open("./key.txt","r")
except FileNotFoundError as e:
    raise Exception('Error: key.txt file not found')

k=f.read().rstrip("\n")
f.close()

try:
    f2=open("./secret.txt","r")
except FileNotFoundError as e:
    raise Exception('Error: secret.txt file not found')

s=f2.read().rstrip("\n")
f2.close()

@app.route("/")
def home():
    session = authlib.client.OAuth2Session(k, s,redirect_uri='http://localhost:5000')

    uri,state=session.authorization_url(AUTHORIZATION_URL)

    flask.session["auth_state"]=state
    flask.session.permanent=True

    return flask.redirect(uri,code=302)

@app.route("/second")
def redirect():
    state=flask.request.args.get("state",default=None,type=None)

    if state != flask.session["auth_state"]:
        return flask.render_template("j.html",something="Uhh you done messed up")
    session = authlib.client.OAuth2Session(k, s,redirect_uri='http://localhost:5000')

    oauth2_tokens = session.fetch_access_token(ACCESS_TOKEN_URI,authorization_response=flask.request.url)

    flask.session[AUTH_TOKEN_KEY]=oauth2_tokens

    return flask.render_template("j.html",oauth_tokens)
