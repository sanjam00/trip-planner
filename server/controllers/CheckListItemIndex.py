from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList, CheckListItem
from models.schemas import CheckListItemSchema

class CheckListItemIndex(Resource):

  # add a new item to a checklist
  @jwt_required()
  def post(self, trip_id, checklist_id):
    # confirms the checklist belongs (via trip) to this user before adding to it
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == checklist_id, CheckList.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
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