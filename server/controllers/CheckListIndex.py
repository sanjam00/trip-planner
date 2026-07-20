from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList
from models.schemas import CheckListSchema

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