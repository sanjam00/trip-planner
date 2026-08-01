from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList, CheckListItem, Status
from models.schemas import CheckListItemSchema

class CheckListItemById(Resource):

  # edit an item (e.g. flip status to packed)
  @jwt_required()
  def patch(self, trip_id, checklist_id, id):
    item = CheckListItem.query.join(CheckList).join(Trip).filter(
      CheckListItem.id == id,
      CheckListItem.checklist_id == checklist_id,
      Trip.id == trip_id,
      Trip.user_id == int(get_jwt_identity())
    ).first()

    if not item:
      return {'error': '404 Checklist item not found'}, 404

    request_json = request.get_json()

    if 'item_name' in request_json:
      item.item_name = request_json['item_name']
    if 'status' in request_json:
      try:
        item.status = Status(request_json['status'])
      except ValueError:
        return {'errors': [f"Invalid status. Must be one of: {[s.value for s in Status]}"]}, 422

    db.session.commit()
    return CheckListItemSchema().dump(item), 200

  # delete an item
  @jwt_required()
  def delete(self, trip_id, checklist_id, id):
    item = CheckListItem.query.join(CheckList).join(Trip).filter(
      CheckListItem.id == id,
      CheckListItem.checklist_id == checklist_id,
      Trip.id == trip_id,
      Trip.user_id == int(get_jwt_identity())
    ).first()

    if not item:
      return {'error': '404 Checklist item not found'}, 404

    db.session.delete(item)
    db.session.commit()

    return {'200': 'Checklist item successfully deleted'}, 200
