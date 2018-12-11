import json
from urllib2 import Request, urlopen, URLError
from flask import session
from flask_oauth import OAuth
from pvtranslator.models.user import User

GOOGLE_CLIENT_ID = '827082594735-u8qer289a8oelkr1h02cuc1tcpmv93ic.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'UAMh_YXZhCKqwp1HNiw2Rh8L'
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


def get_user():
    access_token = session.get('access_token')
    if access_token is None:
        return None

    access_token = access_token[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return None
        return None
    request_result = json.loads(res.read())
    user_id = request_result['id']
    user_email = request_result['email']
    user_name = request_result['name']
    users = User.search_by_id(user_id)
    if len(users)>0:
        result_user = users[0]
    else:
        result_user = User(id=user_id, email=user_email, name=user_name)
        result_user.put()
    return result_user
