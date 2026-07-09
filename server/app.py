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
  @jwt_required()
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
      db.session.add(trip)
      db.session.commit()
      return TripSchema().dump(trip), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class TripById(Resource):

  # get by id
  @jwt_required()
  def get(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == get_jwt_identity() ).first()

    if not trip:
      return { 'errors': '404 Trip not found' }, 404
    
    return TripSchema().dump(trip), 200

  # edit a trip
  @jwt_required()
  def patch(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == get_jwt_identity() ).first()

    if not trip:
      return {'error': '404 Trip not found'}, 404
    
    request_json = request.get_json()

    if 'title' in request_json:
      trip.title = request_json['title']
    if 'description' in request_json:
      trip.description = request_json['description']
    if 'destination' in request_json:
      trip.destination = request_json['destination']
    if 'start_date' in request_json:
      trip.start_date = request_json['start_date']
    if 'end_date' in request_json:
      trip.end_date = request_json['end_date']
    if 'notes' in request_json:
      trip.notes = request_json['notes']

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

    return {'200': 'Trip successfully deleted'}, 200
  
class CheckListIndex(Resource):

  # get multiple checklists
  @jwt_required()
  def get(self):
    # requires login, gets user id from login
    user_id = get_jwt_identity()

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # dynamic pagination
    pagination = CheckList.query.join(Trip).filter(
    Trip.user_id == user_id
    ).paginate(page=page, per_page=per_page, error_out=False)

    checklist = pagination.items

    return {
      'trips': CheckListSchema(many=True).dump(checklist),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200

  # add a new checklist
  @jwt_required()
  def post(self, trip_id):
    request_json = request.get_json()

    checklist = CheckList(
      title=request_json.get('title'),
      trip_id=trip_id
    )

    try:
      db.session.add(checklist)
      db.session.commit()
      return CheckListSchema().dump(checklist), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class CheckListById(Resource):
  # get by id
  @jwt_required()
  def get(self, id):
    checklist = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first()

    if not checklist:
      return { 'errors': '404 Checklist not found' }, 404
    
    return CheckListSchema().dump(checklist), 200

  # edit a list
  @jwt_required()
  def patch(self, id):
    checklist = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first()

    if not checklist:
      return {'error': '404 Checklist not found'}, 404
    
    request_json = request.get_json()

    if 'title' in request_json:
      checklist.title = request_json['title']

    db.session.commit()

    return CheckListSchema().dump(checklist), 200

  # delete a checklist
  @jwt_required()
  def delete(self, id):
    checklist = CheckList.query.filter( CheckList.id == id, CheckList.user_id == get_jwt_identity() ).first()

    if not checklist:
      return {'error': '404 Checklist not found'}, 404
    
    db.session.delete(checklist)
    db.session.commit()

    return {'200': 'Checklist successfully deleted'}, 200

class ItineraryListIndex(Resource):
  # get multiple itineraries
  @jwt_required()
  def get(self):
    # requires login, gets user id from login
    user_id = get_jwt_identity()

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # dynamic pagination
    pagination = ItineraryList.query.join(Trip).filter(
    Trip.user_id == user_id
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
  def post(self, trip_id):
    request_json = request.get_json()

    itin = ItineraryList(
      title=request_json.get('title'),
      trip_id=trip_id
    )

    try:
      db.session.add(itin)
      db.session.commit()
      return ItineraryListSchema().dump(itin), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class ItineraryListById(Resource):
  # get by id
  @jwt_required()
  def get(self, id):
    itin_list = ItineraryList.query.filter( ItineraryList.id == id, ItineraryList.user_id == get_jwt_identity() ).first()

    if not itin_list:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    return ItineraryListSchema().dump(itin_list), 200

  # edit an itinerary list
  @jwt_required()
  def patch(self, id):
    itin_list = ItineraryList.query.filter( ItineraryList.id == id, ItineraryList.user_id == get_jwt_identity() ).first()

    if not itin_list:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    request_json = request.get_json()

    if 'title' in request_json:
      itin_list.title = request_json['title']

    db.session.commit()

    return ItineraryListSchema().dump(itin_list), 200

  # delete a trip
  @jwt_required()
  def delete(self, id):
    itin_list = ItineraryList.query.filter( ItineraryList.id == id, ItineraryList.user_id == get_jwt_identity() ).first()

    if not itin_list:
      return { 'errors': '404 Itinerary Item not found' }, 404
    
    db.session.delete(itin_list)
    db.session.commit()

    return {'200': 'Itinerary List successfully deleted'}, 200