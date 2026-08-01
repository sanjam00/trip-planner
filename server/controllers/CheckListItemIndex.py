from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList, CheckListItem, Status
from models.schemas import CheckListItemSchema

class CheckListItemIndex(Resource):

  # add a new item to a checklist
  @jwt_required()
  def post(self, trip_id, checklist_id):
    checklist = CheckList.query.join(Trip).filter(
      # confirms the checklist belongs (via trip) to this user before adding to it
      CheckList.id == checklist_id, CheckList.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
    ).first()
    if not checklist:
      return {'error': '404 Checklist not found'}, 404

    request_json = request.get_json()
    status_value = request_json.get('status', 'not packed')

    try:
      status = Status(status_value)
    except ValueError:
      return {'errors': [f"Invalid status. Must be one of: {[s.value for s in Status]}"]}, 422

    item = CheckListItem(
      item_name=request_json.get('item_name'),
      status=status,
      checklist_id=checklist_id
    )

    try:
      db.session.add(item)
      db.session.commit()
      return CheckListItemSchema().dump(item), 201
    except IntegrityError:
      db.session.rollback()
      return {'errors': ['422 Unprocessable Entity']}, 422