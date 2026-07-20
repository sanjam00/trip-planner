from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList, CheckListItem
from models.schemas import CheckListItemSchema

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
