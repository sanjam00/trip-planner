from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, ItineraryItem
from models.schemas import ItineraryItemSchema

class ItineraryItemById(Resource):
  # get by id
  # ItineraryItem has no user_id of its own, so ownership is checked by joining through Trip
  @jwt_required()
  def get(self, trip_id, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, ItineraryItem.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
    ).first()

    if not item:
      return { 'errors': '404 Itinerary item not found' }, 404

    return ItineraryItemSchema().dump(item), 200

  # edit an itinerary item
  @jwt_required()
  def patch(self, trip_id, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, ItineraryItem.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
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
  def delete(self, trip_id, id):
    item = ItineraryItem.query.join(Trip).filter(
      ItineraryItem.id == id, ItineraryItem.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
    ).first()

    if not item:
      return { 'errors': '404 Itinerary item not found' }, 404

    db.session.delete(item)
    db.session.commit()

    return {'200': 'Itinerary item successfully deleted'}, 200