from flask import make_response, jsonify, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from config import db
from models import User
from models.schemas import UserSchema

class Signup(Resource):

  # sign up, create new users
  def post(self):
    request_json = request.get_json()

    username = request_json.get('username')
    email = request_json.get('email')
    password = request_json.get('password')

    # password confirmation
    password_confirmation = request_json.get('password_confirmation')
    if password != password_confirmation:
      return {'error': 'Passwords do not match'}, 400

    user = User(
      username = username,
      email = email
    )
    user.password_hash = password

    try:
      db.session.add(user)
      db.session.commit()
      access_token = create_access_token(identity=user.id)
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422
