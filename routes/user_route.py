from __init__ import Users, jsonify, request, generate_password_hash, db, app
from app import token_required


@app.route('/api/user', methods=['GET'])
@token_required
def get_all_user(current_user):
    users = Users.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users': output})


@app.route('/api/user/<user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    user = Users.query.filter_by(user_id = user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['user_id'] = user.user_id
    user_data['username'] = user.username
    user_data['password'] = user.password

    return jsonify({'user': user_data})


@app.route('/api/user/<user_id>', methods=['PUT'])
@token_required
def promote_user(current_user, user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    return ''


@app.route('/api/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user have been delete'})

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print("data: ", data)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(username = data['username'], password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created'})
