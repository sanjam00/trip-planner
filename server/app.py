from flask import make_response, jsonify, request
from flask_restful import Resource # using resource allows for compartmentalization, grouping routes together
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from config import app, db, jwt, api
from models import (
  User, UserSchema,
  Trip, TripSchema,
  CheckList, CheckListSchema,
  CheckListItem, CheckListItemSchema,
  ItineraryItem, ItineraryItemSchema
  )

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

  # get multiple checklists for a trip
  # registered at /trips/<int:trip_id>/checklists, so trip_id always comes from the route
  @jwt_required()
  def get(self, trip_id):
    user_id = get_jwt_identity()

    # confirms the trip belongs to this user before showing its checklists
    trip = Trip.query.filter( Trip.id == trip_id, Trip.user_id == user_id ).first()
    if not trip:
      return {'error': '404 Trip not found'}, 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = CheckList.query.filter(
      CheckList.trip_id == trip_id
    ).paginate(page=page, per_page=per_page, error_out=False)

    checklists = pagination.items

    return {
      'checklists': CheckListSchema(many=True).dump(checklists),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200

  # add a new checklist to a trip
  @jwt_required()
  def post(self, trip_id):
    # confirms the trip belongs to this user before adding to it
    trip = Trip.query.filter( Trip.id == trip_id, Trip.user_id == get_jwt_identity() ).first()
    if not trip:
      return {'error': '404 Trip not found'}, 404

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
  # CheckList has no user_id of its own, so ownership is checked by joining through Trip
  @jwt_required()
  def get(self, id):
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not checklist:
      return { 'errors': '404 Checklist not found' }, 404

    return CheckListSchema().dump(checklist), 200

  # edit a list
  @jwt_required()
  def patch(self, id):
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, Trip.user_id == get_jwt_identity()
    ).first()

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
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not checklist:
      return {'error': '404 Checklist not found'}, 404

    db.session.delete(checklist)
    db.session.commit()

    return {'200': 'Checklist successfully deleted'}, 200

class CheckListItemIndex(Resource):

  # add a new item to a checklist
  @jwt_required()
  def post(self, checklist_id):
    # confirms the checklist belongs (via trip) to this user before adding to it
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == checklist_id, Trip.user_id == get_jwt_identity()
    ).first()
    if not checklist:
      return {'error': '404 Checklist not found'}, 404

    request_json = request.get_json()

    item = CheckListItem(
      item_name=request_json.get('item_name'),
      status=request_json.get('status', 'not packed'),
      checklist_id=checklist_id
    )

    try:
      db.session.add(item)
      db.session.commit()
      return CheckListItemSchema().dump(item), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class CheckListItemById(Resource):

  # edit an item (e.g. flip status to packed)
  @jwt_required()
  def patch(self, id):
    item = CheckListItem.query.join(CheckList).join(Trip).filter(
      CheckListItem.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not item:
      return {'error': '404 Checklist item not found'}, 404

    request_json = request.get_json()

    if 'item_name' in request_json:
      item.item_name = request_json['item_name']
    if 'status' in request_json:
      item.status = request_json['status']

    db.session.commit()

    return CheckListItemSchema().dump(item), 200

  # delete an item
  @jwt_required()
  def delete(self, id):
    item = CheckListItem.query.join(CheckList).join(Trip).filter(
      CheckListItem.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not item:
      return {'error': '404 Checklist item not found'}, 404

    db.session.delete(item)
    db.session.commit()

    return {'200': 'Checklist item successfully deleted'}, 200

class ItineraryItemIndex(Resource):

  # get all itinerary items for a trip
  @jwt_required()
  def get(self, trip_id):
    user_id = get_jwt_identity()

    trip = Trip.query.filter( Trip.id == trip_id, Trip.user_id == user_id ).first()
    if not trip:
      return {'error': '404 Trip not found'}, 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = ItineraryItem.query.filter(
      ItineraryItem.trip_id == trip_id
    ).paginate(page=page, per_page=per_page, error_out=False)

    items = pagination.items

    return {
      'itinerary_items': ItineraryItemSchema(many=True).dump(items),
      'total_pages': pagination.pages,
      'current_page': page,
      'has_next': pagination.has_next,
      'has_prev': pagination.has_prev
      }, 200

  # add a new itinerary item to a trip
  @jwt_required()
  def post(self, trip_id):
    trip = Trip.query.filter( Trip.id == trip_id, Trip.user_id == get_jwt_identity() ).first()
    if not trip:
      return {'error': '404 Trip not found'}, 404

    request_json = request.get_json()

    item = ItineraryItem(
      activity=request_json.get('activity'),
      start_time=request_json.get('start_time'),
      end_time=request_json.get('end_time'),
      day=request_json.get('day'),
      trip_id=trip_id
    )

    try:
      db.session.add(item)
      db.session.commit()
      return ItineraryItemSchema().dump(item), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422

class ItineraryItemById(Resource):
  # get by id
  # ItineraryItem has no user_id of its own, so ownership is checked by joining through Trip
  @jwt_required()
  def get(self, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not item:
      return { 'errors': '404 Itinerary item not found' }, 404

    return ItineraryItemSchema().dump(item), 200

  # edit an itinerary item
  @jwt_required()
  def patch(self, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not item:
      return { 'errors': '404 Itinerary item not found' }, 404

    request_json = request.get_json()

    if 'activity' in request_json:
      item.activity = request_json['activity']
    if 'start_time' in request_json:
      item.start_time = request_json['start_time']
    if 'end_time' in request_json:
      item.end_time = request_json['end_time']
    if 'day' in request_json:
      item.day = request_json['day']

    db.session.commit()

    return ItineraryItemSchema().dump(item), 200

  # delete an itinerary item
  @jwt_required()
  def delete(self, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, Trip.user_id == get_jwt_identity()
    ).first()

    if not item:
      return { 'errors': '404 Itinerary item not found' }, 404

    db.session.delete(item)
    db.session.commit()

    return {'200': 'Itinerary item successfully deleted'}, 200

# --- routes ---
# checklists and itinerary items are nested under a trip since they can't exist without one

api.add_resource(Signup, '/signup')
api.add_resource(WhoAmI, '/whoami')
api.add_resource(Login, '/login')

api.add_resource(TripIndex, '/trips')
api.add_resource(TripById, '/trips/<int:id>')

api.add_resource(CheckListIndex, '/trips/<int:trip_id>/checklists')
api.add_resource(CheckListById, '/checklists/<int:id>')
api.add_resource(CheckListItemIndex, '/checklists/<int:checklist_id>/items')
api.add_resource(CheckListItemById, '/checklist-items/<int:id>')

api.add_resource(ItineraryItemIndex, '/trips/<int:trip_id>/itinerary-items')
api.add_resource(ItineraryItemById, '/itinerary-items/<int:id>')