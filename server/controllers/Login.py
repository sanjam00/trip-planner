from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import User
from models.schemas import UserSchema

class Login(Resource):

  # login
  def post(self):
    username = request.json['username']
    password = request.json['password']

    # find the first username matching the one entered
    user = User.query.filter(User.username == username).first()

    # authenticate user by comparing passwords of the queried user
    if user and user.authenticate(password):
      access_token = create_access_token(identity=user.id)
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)

    return {'errors': ['401 Unauthorized']}, 401