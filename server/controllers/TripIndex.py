from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip
from models.schemas import TripSchema

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