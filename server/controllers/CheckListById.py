from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from config import db
from models import Trip, CheckList
from models.schemas import CheckListSchema

class CheckListById(Resource):
  # get by id
  # CheckList has no user_id of its own, so ownership is checked by joining through Trip
  @jwt_required()
  def get(self, trip_id, id):
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, CheckList.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
    ).first()

    if not checklist:
      return { 'errors': '404 Checklist not found' }, 404

    return CheckListSchema().dump(checklist), 200

  # edit a list
  @jwt_required()
  def patch(self, trip_id, id):
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, CheckList.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
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
  def delete(self, trip_id, id):
    checklist = CheckList.query.join(Trip).filter(
      CheckList.id == id, CheckList.trip_id == trip_id, Trip.user_id == int(get_jwt_identity())
    ).first()

    if not checklist:
      return {'error': '404 Checklist not found'}, 404

    db.session.delete(checklist)
    db.session.commit()

    return {'200': 'Checklist successfully deleted'}, 200