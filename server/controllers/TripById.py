from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

from config import db
from models import Trip
from models.schemas import TripSchema

class TripById(Resource):

  # get by id
  @jwt_required()
  def get(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == int(get_jwt_identity()) ).first()

    if not trip:
      return { 'errors': '404 Trip not found' }, 404

    return TripSchema().dump(trip), 200

  # edit a trip
  @jwt_required()
  def patch(self, id):
    trip = Trip.query.filter( Trip.id == id, Trip.user_id == int(get_jwt_identity()) ).first()

    if not trip:
      return {'error': '404 Trip not found'}, 404

    request_json = request.get_json()

    try:
      if 'start_date' in request_json:
        trip.start_date = datetime.strptime(request_json['start_date'], '%Y-%m-%d').date()
      if 'end_date' in request_json:
        trip.end_date = datetime.strptime(request_json['end_date'], '%Y-%m-%d').date()
    except (ValueError, TypeError):
      return {'errors': ['Invalid date format, expected YYYY-MM-DD']}, 422

    if 'title' in request_json:
      trip.title = request_json['title']
    if 'description' in request_json:
      trip.description = request_json['description']
    if 'destination' in request_json:
      trip.destination = request_json['destination']
    if 'notes' in request_json:
      trip.notes = request_json['notes']

    db.session.commit()

    return TripSchema().dump(trip), 200

  # delete a trip
  @jwt_required()
  def delete(self, id):
    trip = Trip.query.filter(Trip.id == id, Trip.user_id == int(get_jwt_identity()) ).first()

    if not trip:
      return {'error': '404 Trip not found'}, 404

    db.session.delete(trip)
    db.session.commit()

    return {'200': 'Trip successfully deleted'}, 200