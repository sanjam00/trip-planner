from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import User
from models.schemas import UserSchema

class WhoAmI(Resource):

  # return identity of user, only accessible if logged in
  @jwt_required()
  def get(self):
    user_id = int(get_jwt_identity())
    user = User.query.filter(User.id == user_id).first()
    return UserSchema().dump(user), 200