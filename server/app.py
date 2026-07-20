from flask import make_response, jsonify, request
from flask_restful import Resource # using resource allows for compartmentalization, grouping routes together
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from config import app, db, jwt, api
from models import (
  User,
  Trip,
  CheckList,
  CheckListItem,
  ItineraryItem,
)
from models.schemas import (
  UserSchema,
  TripSchema,
  CheckListSchema,
  CheckListItemSchema,
  ItineraryItemSchema,
)

from config import app, api

from controllers.SignUp import Signup
from controllers.WhoAmI import WhoAmI
from controllers.Login import Login
from controllers.TripIndex import TripIndex
from controllers.TripById import TripById
from controllers.CheckListIndex import CheckListIndex
from controllers.CheckListById import CheckListById
from controllers.CheckListItemIndex import CheckListItemIndex
from controllers.CheckListItemById import CheckListItemById
from controllers.ItineraryItemIndex import ItineraryItemIndex
from controllers.ItineraryItemById import ItineraryItemById

# --- routes ---
# checklists and itinerary items are nested under a trip since they can't exist without one

api.add_resource(Signup, '/signup')
api.add_resource(WhoAmI, '/whoami')
api.add_resource(Login, '/login')

api.add_resource(TripIndex, '/trips')
api.add_resource(TripById, '/trips/<int:id>')

api.add_resource(CheckListIndex, '/trips/<int:trip_id>/checklists')
api.add_resource(CheckListById, '/checklists/<int:id>')
api.add_resource(CheckListItemIndex, '/checklists/<int:checklist_id>/items')
api.add_resource(CheckListItemById, '/checklist-items/<int:id>')

api.add_resource(ItineraryItemIndex, '/trips/<int:trip_id>/itinerary-items')
api.add_resource(ItineraryItemById, '/itinerary-items/<int:id>')