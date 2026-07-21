from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime

from config import db
from models import Trip, ItineraryItem
from models.schemas import ItineraryItemSchema

class ItineraryItemIndex(Resource):

  # get all itinerary items for a trip
  @jwt_required()
  def get(self, trip_id):
    user_id = int(get_jwt_identity())

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
    trip = Trip.query.filter( Trip.id == trip_id, Trip.user_id == int(get_jwt_identity()) ).first()
    if not trip:
      return {'error': '404 Trip not found'}, 404

    request_json = request.get_json()

    try:
      start_time = datetime.strptime(request_json.get('start_time'), '%H:%M:%S').time()
      end_time = datetime.strptime(request_json.get('end_time'), '%H:%M:%S').time()
      day = datetime.strptime(request_json.get('day'), '%Y-%m-%d').date()
    except (ValueError, TypeError):
      return {'errors': ['Invalid date format, expected YYYY-MM-DD']}, 422

    item = ItineraryItem(
      activity=request_json.get('activity'),
      start_time=start_time,
      end_time=end_time,
      day=day,
      trip_id=trip_id
    )

    try:
      db.session.add(item)
      db.session.commit()
      return ItineraryItemSchema().dump(item), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422
