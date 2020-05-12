from __init__ import request, make_response, Users, check_password_hash, jwt, datetime, app, jsonify


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    user = Users.query.filter_by(username = auth.username).first()

    if not user:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'user_id': user.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            app.config['SECRET_KEY']
        )

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})