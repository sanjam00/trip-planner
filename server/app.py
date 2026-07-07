from flask import make_response, jsonify, request, session
from flask_restful import Resource # using resource allows for compartmentalization, grouping routes together
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request, jwt_required

from config import app, db, jwt, api
from models import (
  User, UserSchema, 
  Trip, TripSchema, 
  CheckList, CheckListSchema, 
  CheckListItem, CheckListItemSchema, 
  ItineraryList, ItineraryListSchema, 
  ItineraryItem, ItineraryItemSchema
  )

class Signup(Resource):

  # sign up, create new uers
  def post(self):
    request_json = request.get_json()

    username = request_json.get('username')
    email = request_json.get('email')
    password = request_json.get('password')

    # password confirmation
    password_confirmation = request_json.get('password confirmation')
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
    
class WhoAmI(Resource):

  # return identity of user, only accessible if logged in
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    user = User.query.filter(User.id == user_id).first()
    return UserSchema().dump(user), 200
  
class Login(Resource):

  # login
  def post(self):
    username = request.json['username']
    password = request.json['password']

    # find the first username matching the one entered
    user = User.query.filter(User.username == username).first()

    # authenticate user by comparing passwords of the queried user
    if user and user.authenticated(password):
      access_token = create_access_token(identity=user.id)
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)

    return {'errors': ['401 Unauthorized']}, 401