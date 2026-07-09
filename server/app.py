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
    if user and user.authenticate(password):
      access_token = create_access_token(identity=user.id)
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)

    return {'errors': ['401 Unauthorized']}, 401

class TripIndex(Resource):

  # get multiple trips
  def get(self):
    # requires login, gets user id from login
    user_id = get_jwt_identity()

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # dynamic pagination
    pagination = Trip.query.filter(
      Trip.user_id == user_id   # only trips belonging to that user are returned
    ).paginate(page=page, per_page=per_page, error_out=False)

    trips = pagination.items

    return {
      'trips': TripSchema(many=True).dump(trips),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200
  
  # add a new trip
  @jwt_required()
  def post(self):
    request_json = request.get_json()

    trip = Trip(
      title=request_json.get('title'),
      description=request_json.get('description'),
      destination=request_json.get('destination'),
      start_date=request_json.get('start_date'),
      end_date=request_json.get('end_date'),
      notes=request_json.get('notes'),
      user_id=get_jwt_identity()
    )

    try:
      db.session.add()
      db.session.commit(trip)
      return TripSchema().dump(trip), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class TripById(Resource):

  # get by id
  @jwt_required()
  def get(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == get_jwt_identity() ).first

    if not trip:
      return { 'errors': '404 Trip not found' }, 404
    
    return TripSchema().dump(trip), 200

  # edit a trip
  @jwt_required()
  def patch(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == get_jwt_identity() ).first

    if not trip:
      return {'error': '404 Trip not found'}, 404
    
    request_json = request.get_json()

    if 'title' in request_json:
      trip.title = request_json['title']
    if 'description' in request_json:
      trip.body = request_json['description']
    if 'destination' in request_json:
      trip.body = request_json['destination']
    if 'start_date' in request_json:
      trip.body = request_json['start_date']
    if 'end_date' in request_json:
      trip.body = request_json['end_date']
    if 'notes' in request_json:
      trip.body = request_json['notes']

    db.session.commit()

    return TripSchema().dump(trip), 200

  # delete a trip
  @jwt_required()
  def delete(self, id):
    trip = Trip.query.filter(Trip.id == id, Trip.user_id == get_jwt_identity() ).first()

    if not trip:
      return {'error': '404 Trip not found'}, 404
    
    db.session.delete(trip)
    db.session.commit()

    return {'204': 'Trip successfully deleted'}, 204
  
class CheckListIndex(Resource):

  # get multiple checklists
  def get(self):
    # requires login, gets user id from login
    user_id = get_jwt_identity()

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # dynamic pagination
    pagination = CheckList.query.filter(
      CheckList.user_id == user_id   # only trips belonging to that user are returned
    ).paginate(page=page, per_page=per_page, error_out=False)

    list = pagination.items

    return {
      'trips': CheckListSchema(many=True).dump(list),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200

  # add a new checklist
  def post(self):
    request_json = request.get_json()

    list = CheckList(
      title=request_json.get('title')
    )

    try:
      db.session.add()
      db.session.commit(list)
      return CheckListSchema().dump(list), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class CheckListById(Resource):
  # get by id
  @jwt_required()
  def get(self, id):
    list = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first

    if not list:
      return { 'errors': '404 Checklist not found' }, 404
    
    return CheckListSchema().dump(list), 200

  # edit a list
  @jwt_required()
  def patch(self, id):
    list = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first

    if not list:
      return {'error': '404 Checklist not found'}, 404
    
    request_json = request.get_json()

    if 'title' in request_json:
      list.title = request_json['title']

    db.session.commit()

    return CheckListSchema().dump(list), 200

  # delete a trip
  @jwt_required()
  def delete(self, id):
    list = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first

    if not list:
      return {'error': '404 Checklist not found'}, 404
    
    db.session.delete(list)
    db.session.commit()

    return {'204': 'Checklist successfully deleted'}, 204

class ItineraryIndex(Resource):
  # get multiple itineraries
  def get(self):
    # requires login, gets user id from login
    user_id = get_jwt_identity()

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # dynamic pagination
    pagination = ItineraryList.query.filter(
      ItineraryList.user_id == user_id   # only trips belonging to that user are returned
    ).paginate(page=page, per_page=per_page, error_out=False)

    itin = pagination.items

    return {
      'trips': ItineraryListSchema(many=True).dump(itin),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200
  
  # add a new itin list
  @jwt_required()
  def post(self):
    request_json = request.get_json()

    itin = ItineraryList(
      title=request_json.get('title'),
    )

    try:
      db.session.add()
      db.session.commit(itin)
      return ItineraryListSchema().dump(itin), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class ItineraryItemById(Resource):
  # get by id
  @jwt_required()
  def get(self, id):
    itin_item = ItineraryItem.query.filter( ItineraryItem.id == id, ItineraryItem.user_id == get_jwt_identity() ).first

    if not itin_item:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    return ItineraryItemSchema().dump(itin_item), 200

  # edit am itinerary
  @jwt_required()
  def patch(self, id):
    itin_item = ItineraryItem.query.filter( ItineraryItem.id == id, ItineraryItem.user_id == get_jwt_identity() ).first

    if not itin_item:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    request_json = request.get_json()

    if 'activity' in request_json:
      itin_item.title = request_json['activity']
    if 'start_time' in request_json:
      itin_item.body = request_json['start_time']
    if 'end_time' in request_json:
      itin_item.body = request_json['end_time']
    if 'day' in request_json:
      itin_item.body = request_json['day']

    db.session.commit()

    return ItineraryItemSchema().dump(itin_item), 200

  # delete a trip
  @jwt_required()
  def delete(self, id):
    itin_item = ItineraryItem.query.filter( ItineraryItem.id == id, ItineraryItem.user_id == get_jwt_identity() ).first

    if not itin_item:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    db.session.delete(itin_item)
    db.session.commit()

    return {'204': 'Itinerary Item successfully deleted'}, 204